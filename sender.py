from common import *

class sender:
    RTT = 20
    
    def isCorrupted(self, packet):
        '''Checks if a received packet (acknowledgement) has been corrupted
        during transmission.
        Return true if computed checksum is different than packet checksum.
        '''
        if packet.checksum != checksumCalc(packet.payload):
            return True
        return False

    def isDuplicate(self, packet):
        '''checks if an acknowledgement packet is duplicate or not
        similar to the corresponding function in receiver side
        '''
        if packet.ackNum != self.seqNum:
            return True
        return False
 
    def getNextSeqNum(self):
        '''generate the next sequence number to be used.
        '''
        if self.seqNum == 0:
            return 1
        else:
            return 0

    def __init__(self, entityName, ns):
        self.entity = entityName
        self.networkSimulator = ns
        print("Initializing sender: A: "+str(self.entity))

    def init(self):
        '''initialize the sequence number and the packet in transit.
        Initially there is no packet is transit and it should be set to None
        '''
        self.seqNum = 0
        self.ackNum = 0
        self.inTransit = None
        return

    def timerInterrupt(self):
        '''This function implements what the sender does in case of timer
        interrupt event.
        This function sends the packet again, restarts the time, and sets
        the timeout to be twice the RTT.
        You never call this function. It is called by the simulator.
        '''
        self.networkSimulator.udtSend(self.entity, self.inTransit)
        self.networkSimulator.startTimer(self.entity, RTT*2)
        return


    def output(self, message):
        '''prepare a packet and send the packet through the network layer
        by calling calling utdSend.
        It also start the timer.
        It must ignore the message if there is one packet in transit
        '''
        if self.inTransit is not None:
            packet = Packet(self.seqNum, self.ackNum, checksumCalc(message.data), message.data)
            print('udtSend: seqNum: {0} ackNum: {1} checksum: {2} payload: {3}'.format(packet.seqNum, packet.ackNum, packet.checksum, packet.payload))
            self.networkSimulator.udtSend(self.entity, packet)
            print('startTimer: starting timer at {}'.format(self.networkSimulator.time))
            self.networkSimulator.startTimer(self.entity, RTT*2)
            self.inTransit = packet
        return
 
    
    def input(self, packet):
        '''If the acknowlegement packet isn't corrupted or duplicate, 
        transmission is complete. Therefore, indicate there is no packet
        in transition.
        The timer should be stopped, and sequence number  should be updated.

        In the case of duplicate or corrupt acknowlegement packet, it does 
        not do anything and the packet will be sent again since the
        timer will be expired and timerInterrupt will be called by the simulator.
        '''
        if not (isCorrupted(packet) or isDuplicate(packet)):
            print('stopTimer: stopping timer at {}'.format(self.networkSimulator.time))
            stopTimer(self.entity)
            self.inTransit = None
            self.ackNum = packet.ackNum
            self.seqNum = getNextSeqNum()
        return 
