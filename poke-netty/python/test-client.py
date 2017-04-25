import comm_pb2
import struct
import sys
import socket
import time
import json


def serialize_and_send(request):
	#Serialize Protobuf
	s = request.SerializeToString()
	packed_len = struct.pack('>L', len(s))

	#Socket Connection
	sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server_address=('localhost',5570)
	print('connecting to %s port %s' %server_address)
	sock.connect(server_address)
	print 'sending message'
	sock.sendall(packed_len + s)

	# Receive at s, a message of type Request and close connection
	return get_message(sock, comm_pb2.Request)
	sock.close()


#Request from the User
def handle_signUp():
	email = raw_input("Enter Email ID: ")
	fname = raw_input("Enter First Name: ")
	lname = raw_input("Enter Last Name: ")
	password = raw_input("Enter Password: ")

	#Build for SignUp 
	request = comm_pb2.Request()
	request.header.routing_id = request.header.JOBS
	request.header.originator = "client"
	request.header.tag = "header for signup"
	request.header.time = long(time.time())
	request.header.toNode = "zero" # Sending to node with node.id "zero"
	request.body.job_op.action = request.body.job_op.ADDJOB
	request.body.job_op.data.name_space = "signup"
	request.body.job_op.data.owner_id = 1
	request.body.job_op.data.job_id = "signup"
	request.body.job_op.data.status = request.body.job_op.data.JOBQUEUED

	request.body.job_op.data.options.node_type = request.body.job_op.data.options.NODE
	nvm1 = request.body.job_op.data.options.node.add()
	nvm1.name = "fname"
	nvm1.value = fname
	nvm1.node_type = request.body.job_op.data.options.VALUE

	nvm2 = request.body.job_op.data.options.node.add()
	nvm2.name = "lname"
	nvm2.value = lname
	nvm2.node_type = request.body.job_op.data.options.VALUE

	nvm3 = request.body.job_op.data.options.node.add()
	nvm3.name = "email"
	nvm3.value = email
	nvm3.node_type = request.body.job_op.data.options.VALUE

	nvm4 = request.body.job_op.data.options.node.add()
	nvm4.name = "password"
	nvm4.value = password
	nvm4.node_type = request.body.job_op.data.options.VALUE

	response = serialize_and_send(request)
	print response

def handle_signin():
	email = raw_input("Enter Email ID: ")
	password = raw_input("Enter Password: ")

	request = comm_pb2.Request()
	request.header.routing_id = request.header.JOBS
	request.header.originator = "client"
	request.header.tag = "header for signup"
	request.header.time = long(time.time())
	request.header.toNode = "zero" # Sending to node with node.id "zero"
	request.body.job_op.action = request.body.job_op.ADDJOB
	request.body.job_op.data.name_space = "signin"
	request.body.job_op.data.owner_id = 1
	request.body.job_op.data.job_id = "signin"
	request.body.job_op.data.status = request.body.job_op.data.JOBQUEUED

	request.body.job_op.data.options.node_type = request.body.job_op.data.options.NODE
	nvm3 = request.body.job_op.data.options.node.add()
	nvm3.name = "email"
	nvm3.value = email
	nvm3.node_type = request.body.job_op.data.options.VALUE

	nvm4 = request.body.job_op.data.options.node.add()
	nvm4.name = "password"
	nvm4.value = password
	nvm4.node_type = request.body.job_op.data.options.VALUE

	response = serialize_and_send(request)
	print response

def handle_list():
	#Build for ListFiles
	request = comm_pb2.Request()
	#Header
	request.header.routing_id = request.header.JOBS
	request.header.originator = "client"
	request.header.tag = "header for list Files"
	request.header.time = long(time.time())
	request.header.toNode = "zero" # Sending to node with node.id "zero"
	#Payload
	request.body.job_op.action = request.body.job_op.ADDJOB
	request.body.job_op.data.name_space = "listcourses"
	request.body.job_op.data.owner_id = 1
	request.body.job_op.data.job_id = "listcourses"
	request.body.job_op.data.status = request.body.job_op.data.JOBQUEUED 

	response = serialize_and_send(request)
	#Parsing Protobuf File
	total_courses = len(response.body.job_op.data.options.node)

	print "List Of Course ::"
	print "##################################"
	for i in range(0,total_courses ):
		print response.body.job_op.data.options.node[i].value
	print "##################################"


#Handle Request for Desc
def handle_desc():
	#Build for Get Desc
	course_value = raw_input("Enter Course Name for which Desc has to be received : ")

	request = comm_pb2.Request()
	#Header
	request.header.routing_id = request.header.JOBS
	request.header.originator = "client"
	request.header.tag = "header for desc Files"
	request.header.time = long(time.time())
	request.header.toNode = "zero" # Sending to node with node.id "zero"
	#Payload
	request.body.job_op.action = request.body.job_op.ADDJOB
	request.body.job_op.data.name_space = "coursedescription"
	request.body.job_op.data.owner_id = 1
	request.body.job_op.data.job_id = "coursedescription"
	request.body.job_op.data.status = request.body.job_op.data.JOBQUEUED
	request.body.job_op.data.options.name = "coursename"
	request.body.job_op.data.options.value = course_value
	request.body.job_op.data.options.node_type = request.body.job_op.data.options.VALUE
	#Serialize Data
	response = serialize_and_send(request)

	print "##################################"
	print course_value + "::" +response.body.job_op.data.options.value
	print "##################################"

def get_message(sock, msgtype):
    """ Read a message from a socket. msgtype is a subclass of
        of protobuf Message.
    """
    len_buf = socket_read_n(sock, 4)
    msg_len = struct.unpack('>L', len_buf)[0]
    msg_buf = socket_read_n(sock, msg_len)

    msg = msgtype()
    msg.ParseFromString(msg_buf)
    return msg

def socket_read_n(sock, n):
    """ Read exactly n bytes from the socket.
        Raise RuntimeError if the connection closed before
        n bytes were read.
    """
    buf = ''
    while n > 0:
        data = sock.recv(n)
        if data == '':
            raise RuntimeError('unexpected connection close')
        buf += data
        n -= len(data)
    return buf


#User selection Option
# Main
def main():
	while 1:
	    selection = raw_input("\n 1.SignUp 2.SignIn 3.List 4.Desc \n")
	    if selection == '1':
		handle_signUp()
	    elif selection == '2':
		handle_signin()
	    elif selection == '3':
		handle_list()
	    elif selection == '4':
		handle_desc()
	    else : 
		print "Enter Valid Input"

if __name__ == '__main__':
    main()