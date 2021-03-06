import serial

def initComm(port):
        """Set up communication via wifly module"""
        comm = serial.Serial()
        comm.port = port
        comm.baudrate = 57600
        comm.bytesize = serial.EIGHTBITS
        comm.parity = serial.PARITY_NONE
        comm.stopbits = serial.STOPBITS_ONE
        comm.writeTimeout = 2 # Non-blocking write.
        comm.timeout = 1 # Non-blocking read.
        comm.xonxoff = False # Disable software flow control
        # Disable hardware flow control
        comm.rtscts = False 
        comm.dsrdtr = False

        try:
		pass 
                comm.open()
                print("Openning communication")
                comm.flushOutput()
        except Exception, e:
                print "error open serial port: " + str(e)
                exit()

        return comm

def sendMessage(sequenceNum, field1, field2, comm):
        """Send message from a simulated unit to control."""

        comm.write(chr(128)) # Send the start byte.
        comm.write(chr(sequenceNum))

        if field1 == None or field2 == None: # NACK
                for i in range(8):
                        comm.write(chr(0))
                return 
        
        # Ensure the values being sent are in the required range
        if field1 > 9999:
                field1 = 9999
        if field2 > 9999:
                field2 = 9999

        field1 = int(field1)
        field2 = int(field2)

        print("field 1", field1)
        print("field 2", field2)
        comm.write(str(field1).zfill(4) + str(field2).zfill(4))

def receiveMessage(comm):
        """Rover receives message from control"""
        msg = comm.read(10)
        # Parse out the fields.
        field1 = float(msg[2])*1000 + float(msg[3])*100 + float(msg[4])*10 + float(msg[5])
        field2 = float(msg[6])*1000 + float(msg[7])*100 + float(msg[8])*10 + float(msg[9])
        comm.flushInput()
        return (field1, field2)



