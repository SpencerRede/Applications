Implementation of a Localhost Peer-to-Peer file sharing network

Tracker program listens to localhost w/ specified port and maintains
    - List of Clients connected w/ hashes of folders they posess

Client program connects with inputted args:
    - folderName: directory they are allowing to be accessed by the peer-to-peer network
    - transferPort: port # associated with client
    - name: Client's Name

    A Client must
        - Read from the specified directory
        - Connect to P2PTracker
        - Sends list of files in directory to P2PTracker

    A Client can
        - Query for the location of another file within the P2P network
            WHERE_CHUNKS, {chunk index}
        - Request a file from another client using 
            REQUEST_CHUNK, {chunk index}
        
            If a file is located on another client, the tracker will send the necessary connection information for the P2PClient program to initiate a connteciton with that respective client and hand over the file queried for
