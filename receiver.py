from common import *


class receiver:

    def isCorrupted(self, packet):
        ''' Checks if a received packet has been corrupted during transmission.
        Return true if computed checksum is different than packet checksum.'''
        if packet.checksum != checksumCalc(packet):
            return True
        return False

    def isDuplicate(self, packet):
        '''checks if packet sequence number is the same as expected sequence number'''
        if packet.seqNum != self.expectedSequenceNumber:
            return True
        return False

    def getNextExpectedSeqNum(self):
        '''The expected sequence numbers are 0 or 1'''
        if self.expectedSequenceNumber == 0:
            return 1

        return 0

    def __init__(self, entityName, ns):
        self.entity = entityName
        self.networkSimulator = ns
        print("Initializing receiver: B: " + str(self.entity))

    def init(self):
        '''initialize expected sequence number'''
        # Can we assume that they always start at 0?
        self.expectedSequenceNumber = 0

        return

    def input(self, packet):
        '''This method will be called whenever a packet sent
        from the sender arrives at the receiver. If the received
        packet is corrupted or duplicate, it sends a packet where
        the ack number is the sequence number of the  last correctly
        received packet. Since there is only 0 and 1 sequence numbers,
        you can use the sequence number that is not expected.

        If packet is OK (not a duplicate or corrupted), deliver it to the
        application layer and send an acknowledgement to the sender
        '''

        if (self.isCorrupted(self, packet)) or (self.isDuplicate(self, packet)):
            print("***Wrong Packet***")
            if (packet.seqNum == 0):

                packet.ackNum = 1

                print("udtSend: seqNum: {} ackNum: {} checksum: {} payload: ".format(packet.seqNum, packet.ackNum,
                                                                                     packet.checksum))
                print("udtSend: SIMULATING PACKET BEING CORRUPTED")
                self.networkSimulator.udtSend(self.entity, packet)

            else:
                packet.ackNum = 0
                print("udtSend: seqNum: {} ackNum: {} checksum: {} payload: ".format(packet.seqNum, packet.ackNum,
                                                                                     packet.checksum))
                print("udtSend: SIMULATING PACKET BEING CORRUPTED")
                self.networkSimulator.udtSend(self.entity, packet)
        else:
            packet.ackNum = packet.seqNum
            print("Receiving the data and sending the acknowledgement {}".format(packet.payload))
            print("udtSend: seqNum: {} ackNum: {} checksum: {} payload: ".format(packet.seqNum, packet.ackNum,
                                                                                 packet.checksum))
            self.networkSimulator.udtSend(self.entity, packet)

        return
