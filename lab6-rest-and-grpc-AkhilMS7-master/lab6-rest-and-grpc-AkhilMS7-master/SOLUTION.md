## CSCI Lab 6

### Running REST and gRPC modules on google cloud instances
A MakeFile has been created which lists all the dependencies involved. To enable make command on linux machines, `sudo apt-get install --reinstall make` has to be run on the instance and then `make run` can be executed to download/install all dependencies.

To get the codebase onto instances, I'm uploading a zipped version of the codebase onto the instances and then unzipping them. \
`sudo apt-get install unzip` command has to be run to enable unzipping on linux machines.

Command to generate the gRPC classes : `python3 -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/service.proto` \
Command to run gRPC server: `python3 grpc-server.py` \
Command to run gRPC client: `python3 grpc-client.py <ip> <action = add|rawImage|dotProduct|jsonImage> <iterations = 1000>`\
Command to run REST server: `python3 rest-server.py`\
Command to run REST client: `python3 rest-client.py <ip> <action = add|rawImage|dotProduct|jsonImage> <iterations = 1000>`


### Readings
All measurements are in milliseconds

| Method | Local(ms) | Same-Zone(ms) | Different Region(ms) |
| :----	| ---- | ---- | ---- |
| REST add | 2.61 | 3.73 | 277.2 |
| gRPC add | 0.46 | 0.7 | 136.6 |
| REST rawimg | 4.64 | 11.24 | 1137.4 |
| gRPC rawimg | 8.68 | 9.19 | 158.9 |
| REST dotproduct | 3.4 | 4.22 | 277.8 |
| gRPC dotproduct | 0.58 | 0.72 | 138.4 |
| REST jsonimg | 39.7 | 48.8 | 1274.2 |
| gRPC jsonimg | 24.5 | 27.7 | 175.9 |
| PING | 0.035 | 0.330 | 135 |

### Obervations
- gRPC on a whole was faster than REST. Especially dealing with images & different regions, gRPC was approximately 7 times faster.
- A big reason gRPC is faster is gRPC uses a single TCP connection(Using HTTP/2) for all the queries in a command, however REST creates a new TCP connection for every query which results in a lot of overhead. HTTP/2 has features like binary framing, multiplexing which makes it more efficient.
- Another reason is gRPC uses protocol buffers for transmission whereas REST uses JSON.
- The ping(Network latency) is minimal in local and same zones but it is substantial over different regions. The tests take a longer time(Especially for REST) for the same services when network communication takes place over different regions compared to local/same-zone.
- Even with ping, gRPC across different regions is still fast and is better than REST when comparing local and same-zone values. REST measurements on raw image service increases by more than 100 times whereas gRPC times increase by only 15 times on average
