import signal, sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from functions.queries import QueryFunctions

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

if __name__ == "__main__":
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

    with SimpleXMLRPCServer(('0.0.0.0', PORT), requestHandler=RequestHandler) as server:
        server.register_introspection_functions()
        query_functions = QueryFunctions()
        

        def signal_handler(signum, frame):
            print("received signal")
            server.server_close()

            # perform clean up, etc. here...
            print("exiting, gracefully")
            sys.exit(0)

       

        # signals
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGHUP, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        server.register_function(query_functions.fetch_players_by_country)
        server.register_function(query_functions.lista_paises)
        server.register_function(query_functions.lista_clubes)
        server.register_function(query_functions.fetch_players_by_club)

        

 
        # start the server
        print(f"Starting the RPC Server in port {PORT}...")
        server.serve_forever()
