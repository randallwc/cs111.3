# NAME: Dylan Gunn,William Randall
# EMAIL: dylankgunn@gmail.com,wrandall1000@gmail.com
# ID: 805112866,805167986

import csv
import sys

# import math

bfree = []
ifree = []


class Superblock:  # do dictionary entries for each of these?
    def __init__(self, row):
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


def scan_inodes(inodes, dirents, first, cap):
    allocated = []  # TODO -- name?
    link_count = {}
    parent_dir = {}

    def check_freelist(inodes_t, alloc):
        for inode in inodes_t:
            num = inode.num
            if num != 0:
                alloc.append(num)
                if num in ifree:
                    print(f"ALLOCATED INODE {num} ON FREELIST")
            if inode.file_type == '0' and num not in ifree:
                print(f"UNALLOCATED INODE {num} NOT ON FREELIST")
        for num in range(first, cap):  # TODO -- cap + 1?
            if num in alloc and num in ifree:
                print(f"ALLOCATED INODE {num} ON FREELIST")
            if num not in alloc and num not in ifree:
                print(f"UNALLOCATED INODE {num} NOT ON FREELIST")

    def check_directories(dirents_t, alloc):
        for entry in dirents_t:
            if entry.name != "'.'" and entry.name != "'..'":
                parent_dir[entry.inode] = entry.parent_inode
            if entry.inode > cap or entry.inode <= 0:
                print(
                    f"DIRECTORY INODE {entry.parent_inode} NAME {entry.name} INVALID NODE {entry.inode}")
            elif entry.inode not in alloc:
                print(
                    f"DIRECTORY INODE {entry.parent_inode} NAME {entry.name} UNALLOCATED INODE {entry.inode}")
            else:
                inode = entry.inode
                if inode not in link_count:
                    link_count[inode] = 1
                else:
                    link_count[inode] += 1

    def check_links(inodes_t, counts):
        for inode in inodes_t:
            num = inode.num
            if counts[num] != inode.link_count:
                print(
                    f"INODE {num} HAS {counts[num]} LINKS BUT LINKCOUNT IS {inode.link_count}")

    def check_curr_parent_dir(dirents_t):
        for entry in dirents_t:
            if entry.name == "'.'" and entry.inode != entry.parent_inode:
                print(f"DIRECTORY INODE {entry.parent_inode} \
                NAME '.' LINK TO INODE {entry.inode} SHOULD BE {entry.parent_inode}")
            if entry.name == "'..'" and parent_dir[entry.parent_inode] != entry.inode:
                print(f"DIRECTORY INODE {entry.parent_inode} \
                NAME '..' LINK TO INODE {entry.inode} SHOULD BE {entry.parent_inode}")

    check_freelist(inodes, allocated)
    check_directories(dirents, allocated)
    check_links(inodes, link_count)
    check_curr_parent_dir(dirents)


def main():
    # Get args
    argv = sys.argv

    # Check if more than 1 arg
    if len(argv) != 2:
        sys.stderr.write("Error: Program expects exactly one argument.")
        exit(1)

    # Load CSV
    try:
        csv_f = open(argv[1], 'r')
    except OSError:
        sys.stderr.write("Error: Unable to open specified file.")
        exit(2)

    superblock, group = None, None
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
            sys.stderr.write("Error: Inconcistency in CSV")
            sys.exit(1)

    # TODO -- if not superblock or not group, error?

    scan_blocks()
    scan_inodes(inodes, dirents, superblock.first_inode, superblock.num_inodes)


if __name__ == "__main__":
    main()
