import asyncio
import time
import uuid

import os
import psycopg2

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from utils.csv_to_xml_converter import CSVtoXMLConverter

files_converter = []

def connect_db():
    return psycopg2.connect(user="is",password="is",host="db-xml",database="is")

def get_csv_files_in_input_folder():
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(CSV_INPUT_PATH) for f in filenames if
            os.path.splitext(f)[1] == '.csv']

def generate_unique_file_name(directory):
    return f"{directory}/{str(uuid.uuid4())}.xml"

def convert_csv_to_xml(in_path, out_path):
    converter = CSVtoXMLConverter(in_path)
    xml = converter.to_xml_str()
    file = open(out_path, "w")
    file.write(xml)

    return xml            

class CSVHandler(FileSystemEventHandler):
    def __init__(self, input_path, output_path):
        self._output_path = output_path
        self._input_path = input_path

        # generate file creation events for existing files
        for file in [os.path.join(dp, f) for dp, dn, filenames in os.walk(input_path) for f in filenames]:
            event = FileCreatedEvent(os.path.join(CSV_INPUT_PATH, file))
            event.event_type = "created"
            self.dispatch(event)

    async def convert_csv(self, csv_path):
        # here we avoid converting the same file again
        # !TODO: check converted files in the database
        if csv_path in await self.get_converted_files():
            return

        print(f"new file to convert: '{csv_path}'")

        # we generate a unique file name for the XML file
        xml_path = generate_unique_file_name(self._output_path)

        # we do the conversion
        
        xml = convert_csv_to_xml(csv_path, xml_path)
        print(f"new xml file generated: '{xml_path}'")
        # !TODO: we should store the XML document into the imported_documents table
         # !TODO: once the conversion is done, we should updated the converted_documents tables

        try:
            connection = connect_db()
            cursor = connection.cursor()

            cursor.execute("INSERT INTO public.converted_documents (src, file_size, dst) VALUES (%s, %s, %s);", (csv_path, os.stat(xml_path).st_size , xml_path))
            connection.commit()
            cursor.execute("INSERT INTO public.imported_documents (file_name, xml) VALUES (%s, %s);",(csv_path, xml))
            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
        

    async def get_converted_files(self):
        # !TODO: you should retrieve from the database the files that were already converted before
        connection = None
        cursor = None
        try:
            connection = connect_db()
            cursor = connection.cursor()

            cursor.execute("SELECT src from converted_documents")

            result = cursor.fetchall()

            for file in result:
                files_converter.append(file)


        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()

        return files_converter

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            asyncio.run(self.convert_csv(event.src_path))


if __name__ == "__main__":

    CSV_INPUT_PATH = "/csv"
    XML_OUTPUT_PATH = "/xml"

    # create the file observer
    observer = Observer()
    observer.schedule(
        CSVHandler(CSV_INPUT_PATH, XML_OUTPUT_PATH),
        path=CSV_INPUT_PATH,
        recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()