import asyncio
import time
import uuid

import os


from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from utils.csv_to_xml_converter import CSVtoXMLConverter
from utils.database import Database







def get_csv_files_in_input_folder():
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(CSV_INPUT_PATH) for f in filenames if
            os.path.splitext(f)[1] == '.csv']

def generate_unique_file_name(directory):
    return f"{directory}/{str(uuid.uuid4())}.xml"


def convert_csv_to_xml(in_path, out_path):
    converter = CSVtoXMLConverter(in_path)
    file = open(out_path, "w")
    file.write(converter.to_xml_str())


def import_doc(file_name, xml):
    database = Database()
    database.insert(
    "INSERT INTO imported_documents (file_name, xml) VALUES (%s,%s)", (file_name, xml))
    

def convert_doc(src, dst, filesize):
    database = Database()
    database.insert(
    "INSERT INTO converted_documents(src, dst, file_size) VALUES (%s,%s,%s)", (src, dst, filesize))
    
class CSVHandler(FileSystemEventHandler):
    def __init__(self, input_path, output_path):
        self._output_path = output_path
        self._input_path = input_path

        # generate file creation events for existing files
        for file in [os.path.join(dp, f) for dp, dn, filenames in os.walk(input_path) for f in filenames]:
            event = FileCreatedEvent(os.path.join(CSV_INPUT_PATH, file))
            event.event_type = "created"
            self.dispatch(event)

    async def convert_csv(self, path_csv):
        # here we avoid converting the same file again
        # !TODO: check converted files in the database
        if path_csv in await self.get_converted_files():
            return

        print(f"new file to convert: '{path_csv}'")

        # we generate a unique file name for the XML file
        path_xml = generate_unique_file_name(self._output_path)

        # we do the conversion

        # !TODO: once the conversion is done, we should updated the converted_documents tables
        convert_csv_to_xml(path_csv, path_xml)
        

        try:
            convert_doc(src = path_csv, dst = path_xml, filesize = os.stat(path_xml).st_size)

            with open(path_xml, 'r', encoding='utf-8') as xml_file:
                xml_content = xml_file.read()

            import_doc(file_name = path_csv, xml = xml_content)


            print(f"xml_file was generated: '{path_xml}'")
        except:
            os.remove(path_xml)    

        


    async def get_converted_files(self):
        ficheiros = []
        database = Database()
        for ficheiro in database.selectTudo("SELECT src FROM converted_documents"):
            ficheiros.append(ficheiro[0])

        return ficheiros

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