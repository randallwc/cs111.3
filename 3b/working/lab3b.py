# NAME: Dylan Gunn,William Randall
# EMAIL: dylankgunn@gmail.com,wrandall1000@gmail.com
# ID: 805112866,805167986

import math
import sys
import csv

class Superblock: #do dictionary entries for each of these?
    def __init__(self,row):
        self.num_blocks = int(row[1])
        self.num_inodes = int(row[2])
        self.block_size = int(row[3])
        self.inode_size = int(row[4])
        self.blocks_per_group = int(row[5])
        self.inode_per_group = int(row[6])
        self.first_inode = int(row[7])

class Group:
    def __init__(self, row):
        self.num = int(row[1])
        self.inode_per_group = int(row[3])
        self.inode_tb = int(row[8])

class Inode:
    def __init__(self, row):
        self.num = int(row[1])
        self.file_type = row[2]
        self.mode = int(row[3])
        self.owner = int(row[4])
        self.group = int(row[5])
        self.link_count = int(row[6])
        self.ctime = row[7]
        self.mtime = row[8]
        self.atime = row[9]
        self.file_size = int(row[10])
        self.num_blocks = int(row[11])
        self.directories = []
        self.directories.extend(row[12:24])
        self.indirect_refs = []
        self.indirect_refs.extend(row[24:27])

class Dirent:
    def __init__(self, row):
        self.parent_inode = int(row[1])
        self.log_offset = int(row[2])
        self.inode = int(row[3])
        self.entry_len = int(row[4])
        self.name_len = int(row[5])
        self.name = row[6]

class Indirect:
    def __init__(self, row):
        self.inode_num = int(row[1])
        self.level = int(row[2])
        self.block_offset = int(row[3])
        self.indir_block_num = int(row[4])
        self.ref_block_num = int(row[5])

def scan_blocks():
    pass

def scan_inodes():
    pass

def main():
    # Check args
    if len(sys.argv) != 2:
        sys.stderr.write("Error: Program expects exactly one argument.\n")
        exit(1)

    # Load CSV
    try:
        csv_f = open(argv[1], 'r')
    except:
        sys.stderr.write("Error: Unable to open specified file.\n")
        exit(2)

    superblock, group = None, None
    bfree = []
    ifree = []
    inodes = []
    dirents = []
    indirects = []

    reader = csv.reader(csv_f, delimiter=',')
    for row in reader:
        elem = row[0]
        if elem == "SUPERBLOCK":
            superblock = Superblock(row)
        elif elem == "GROUP":
            group = Group(row)
        elif elem == "BFREE":
            bfree.append(int(row[1]))
        elif elem == "IFREE":
            ifree.append(int(row[1]))
        elif elem == "INODE":
            inodes.append(Inode(row))
        elif elem == "DIRENT":
            dirents.append(Dirent(row))
        elif elem == "INDIRECT":
            indirects.append(Indirect(row))
        else:
            sys.stderr.write("Error: Inconcistency in CSV\n")
            sys.exit(1)

    #if not superblock or not group, error?
    
    scan_blocks()
    scan_inodes(inodes, superblock.first_inode, superblock.num_inodes)
            

if __name__ == "__main__":
    main()