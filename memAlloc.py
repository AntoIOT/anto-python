class Block:
    def __init__(self, size=0, beginAddr=0, pid="<free>"):
        self.beginAddr = beginAddr#FFFFFF#FFFFFF#FFFFFF
        self.size = size
        self.pid = pid
        self.prev = None
        self.next = None
       
    #get the begin address of the block
    def beginAddr(self):
        return self.beginAddr

    #get the end address of the block
    def endAddr(self):
        return self.beginAddr + self.size

	#check whether the block is free or not
    def isFree(self):
        return self.pid == "<free>"

	#set a process to the block
    def setProcess(self, pid):
        self.pid = pid
	
	#make the node as empty
    def setFree(self):
        self.pid = "<free>"

	#shrink the size of the block
    def shrink(self, newsize):
        newblock = Block(self.size-newsize, self.beginAddr+newsize)
        self.size = newsize
        if self.next != None:
            newblock.next = self.next
            self.next.prev = newblock
        self.next = newblock
        newblock.prev = self

class Memory:
    def __init__(self, size):
        self.head = Block(size)
        
	#search for a block by process id
    def search(self, pid):
        curblock = self.head
        while curblock != None:
            if curblock.pid == pid:
                return curblock
            curblock = curblock.next
        return None
    
    #merge given two adjacent blocks
    def merge(self, blockA, blockB):
        blockA.size += blockB.size
        if blockB.next != None:
            blockA.next = blockB.next
            blockB.next.prev = blockA
        else:
            blockA.next = None
        return blockA

	#allocate a process
    def allocate(self, size, pid):
        #check whether the process id is exists or not
        if self.search(pid) != None:
            print(" Sorry. Process is already exists!")
            return
        
        curblock = self.head
        while curblock != None:
            if curblock.isFree() and curblock.size >= size:
                if curblock.size != size:
                    curblock.shrink(size)
                curblock.setProcess(pid)
                print(" {0} Loaded!".format(pid))
                return
            curblock = curblock.next
        print(" Sorry. No space!")

	#terminate the process by process id
    def terminate(self, pid):
        block = self.search(pid)
        if block != None:
            block.setFree()
            if block.prev != None:
                if block.prev.isFree():
                    block = self.merge(block.prev, block)
            if block.next != None:
                if block.next.isFree():
                    self.merge(block, block.next)
            print(" {0} terminated!".format(pid))
        else:
            print(" Sorry. Process not found!")

	#print the current snapshot of the memory
    def snapshot(self):
        curnode = self.head
        print(" Snapshot\n     0+--------+------+")
        while curnode != None:
            print("      | {0:<7}| {1:<5}|".format(curnode.pid, curnode.size))
            print("{0:>6}+--------+------+".format(curnode.beginAddr+curnode.size))
            curnode = curnode.next

#show header and help
helptext = " Allocate  : A [ProcessID] [Size]\n Terminate : T [ProcessID]\n Snapshot  : S\n Help      : H\n Exit      : E/exit"
print("*** MEMORY ALLOCATION PROGRAMME - FIRST FIT ALGORITHM ***")
print(helptext + "\n")

#get user input as a integer
def getInt(msg):
	try:
		return int(raw_input(msg))
	except:
		print(" Invalid input!")
		return getInt(msg)
		
#create the memory and allocate size for the operating system
m = Memory(getInt("Enter memory size: "))
m.allocate(getInt("Enter size for OS: "), 'OS')

#executing the user command
def execute(command):
    com = map(str, command.upper().split())
    try:
        if com[0] == 'A' and len(com) == 3:
            m.allocate(int(com[2]), com[1])
        elif com[0] == 'T' and len(com) == 2:
            m.terminate(com[1])
        elif com[0] == 'S':
            m.snapshot()
        elif com[0] == 'H':
            print(helptext)
        elif com[0] == 'E' or com[0] == 'EXIT':
            exit()
        else:
            print(" Invalid input. Enter 'H' for help.")
    except:
            print(" Invalid input. Enter 'H' for help.")        

#get user input
while True:
    execute(raw_input("\nmemory> "))
