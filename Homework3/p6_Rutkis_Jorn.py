#problem 6 using Claude in VSCode
from __future__ import annotations
import unittest
from testif import testif

class Entry:
    '''base class for a file system entry with a name and an optional parent Entry'''

    def __init__(self, name: str, parent: Entry | None = None) -> None:
        '''initializes the entry with a name string and a parent Entry (None if it has no parent)
        if the parent is a Folder, this entry is also added to the parent's children
        pre: name is a str, parent is an Entry or None'''
        if not isinstance(name, str): #name must be a string
            raise TypeError("name must be a str")
        if parent is not None and not isinstance(parent, Entry): #parent must be an Entry or None
            raise TypeError("parent must be an Entry or None")
        self.name = name
        self._parent = parent #stored with underscore so it does not clash with the parent() method
        if isinstance(parent, Folder): #keeps the parent's children list in sync with the parent link
            parent.add(self)

    def parent(self) -> Entry | None:
        '''returns the parent Entry of this entry, or None if it has no parent'''
        return self._parent

    def size(self) -> int:
        '''returns the size of the entry in bytes; a generic entry has size 0
        child classes override this method'''
        return 0

    def absolute_path(self) -> list[Entry]:
        '''recursively returns the absolute path of this entry as a list of Entry objects,
        starting with this entry, then its parent, and so on, ending with the root entry'''
        if self._parent is None: #base case: root entry, path is just itself
            return [self]
        return [self] + self._parent.absolute_path() #recursive call on the parent

    def __str__(self) -> str:
        '''returns a string representation of the entry using its name and size'''
        return self.name + " (" + str(self.size()) + " bytes)" #size() call is polymorphic


class File(Entry):
    '''a file entry that stores a nonnegative number of bytes used'''

    def __init__(self, name: str, bytes_used: int, parent: Entry | None = None) -> None:
        '''initializes the file with a name, nonnegative bytes_used and a parent Entry
        pre: bytes_used is an int >= 0'''
        if not isinstance(bytes_used, int) or bytes_used < 0: #bytes_used must be a nonnegative int
            raise ValueError("bytes_used must be a nonnegative int")
        self.bytes_used = bytes_used #set before super().__init__ so the file is valid when added to a parent
        super().__init__(name, parent) #base class sets name and parent

    def size(self) -> int:
        '''overrides Entry.size() to return the number of bytes used by the file'''
        return self.bytes_used


class Folder(Entry):
    '''a folder entry that holds a list of child entries (files and/or other folders)'''

    def __init__(self, name: str, parent: Entry | None = None) -> None:
        '''initializes the folder with a name, a parent Entry and an empty list of children'''
        self._children: list[Entry] = [] #created before super().__init__ in case the folder is added to a parent
        super().__init__(name, parent) #base class sets name and parent

    def add(self, entry: Entry) -> None:
        '''adds entry to this folder's list of children and sets this folder as the entry's parent
        if entry was already in another folder, it is moved (removed from that folder's children)
        pre: entry is an Entry'''
        if not isinstance(entry, Entry): #only entries can be children
            raise TypeError("entry must be an Entry")
        old = entry._parent
        if isinstance(old, Folder) and old is not self and entry in old._children: #moving: remove from the old folder
            old._children.remove(entry)
        entry._parent = self #the folder becomes the entry's parent
        if entry not in self._children: #avoids adding the same entry twice
            self._children.append(entry)

    def children(self) -> tuple[Entry, ...]:
        '''returns a tuple with all child entries of this folder'''
        return tuple(self._children)

    def size(self) -> int:
        '''overrides Entry.size() to return the total size of all children, including nested folders'''
        total = 0
        for child in self._children:
            total += child.size() #polymorphism: a nested Folder's size() recurses into its own children
        return total


def total_size(entries: list[Entry]) -> int:
    '''returns the sum of the sizes of all entries, processed through the common Entry interface
    pre: entries is a list of Entry objects (or objects of subclasses of Entry)'''
    total = 0
    for entry in entries:
        total += entry.size() #polymorphism: the correct size() is chosen based on the object's class
    return total

def path_names(entry: Entry) -> list[str]:
    '''returns the names of the entries in the absolute path of entry'''
    return [e.name for e in entry.absolute_path()]

#d)
def find_large_files(entry: Entry, minimum_size: int) -> list[File]:
    '''recursively returns all File objects whose size is at least minimum_size, starting from entry
    - if entry is a File: returns [entry] if entry.size() >= minimum_size, otherwise []
    - if entry is a Folder: returns the large files found in all of its children, including
      nested folders, in the order the children were added (a folder itself is never returned)
    - if entry is a plain Entry (neither File nor Folder): returns []
    pre: entry is an Entry, minimum_size is an int >= 0
    post: returns a new list of File objects, raises ValueError if minimum_size is negative'''
    if not isinstance(minimum_size, int) or minimum_size < 0: #threshold must be a nonnegative int
        raise ValueError("minimum_size must be a nonnegative int")
    if isinstance(entry, File): #base case: a single file
        if entry.size() >= minimum_size:
            return [entry]
        return []
    if isinstance(entry, Folder): #recursive case: collect the large files from every child
        result: list[File] = []
        for child in entry.children():
            result += find_large_files(child, minimum_size) #recursive call on each child
        return result
    return [] #base case: a plain Entry holds no files

#f)
def build_hierarchy() -> dict[str, Entry]:
    '''builds a folder hierarchy four levels deep and returns its entries in a dict keyed by name
    home/
        readme.txt              500
        docs/
            resume.pdf      120,000
            school/
                notes.txt     2,000
                cop4045/
                    hw3.py    8,000
                    lecture.mp4 750,000
        pictures/
            beach.jpg       300,000
            empty/'''
    home = Folder("home")
    readme = File("readme.txt", 500, home)
    docs = Folder("docs", home)
    resume = File("resume.pdf", 120_000, docs)
    school = Folder("school", docs)
    notes = File("notes.txt", 2_000, school)
    cop4045 = Folder("cop4045", school)
    hw3 = File("hw3.py", 8_000, cop4045)
    lecture = File("lecture.mp4", 750_000, cop4045)
    pictures = Folder("pictures", home)
    beach = File("beach.jpg", 300_000, pictures)
    empty = Folder("empty", pictures)
    entries: list[Entry] = [home, readme, docs, resume, school, notes, cop4045, hw3, lecture, pictures, beach, empty]
    return {e.name: e for e in entries}

def demo_hierarchy() -> None:
    '''part f) and g): shows size(), find_large_files() and absolute_path() on the hierarchy from build_hierarchy()'''
    h = build_hierarchy()
    home = h["home"]
    print("f) one call to home.size() adds up files and folders at every level:", home.size(), "bytes")
    for name in ["docs", "school", "cop4045", "pictures", "empty"]:
        print("   ", name, "size:", h[name].size()) #same size() call works on every folder
    for threshold in [100_000, 5_000]:
        large = find_large_files(home, threshold)
        print("f) files >=", threshold, "bytes:", [str(f) for f in large])
    print("g) absolute_path() of each entry (entry first, root last):")
    for entry in h.values():
        print("   ", entry.name, "->", path_names(entry))


#e)
class TestFindLargeFiles(unittest.TestCase):
    '''unit tests for find_large_files()'''

    def setUp(self) -> None:
        '''builds a fresh hierarchy before every test'''
        self.h = build_hierarchy()

    def test_file_above_minimum(self) -> None:
        '''a file larger than the minimum returns a list with only that file'''
        self.assertEqual(find_large_files(self.h["hw3.py"], 1_000), [self.h["hw3.py"]])

    def test_file_equal_to_minimum(self) -> None:
        '''a file whose size equals the minimum counts as large (at least minimum_size)'''
        self.assertEqual(find_large_files(self.h["hw3.py"], 8_000), [self.h["hw3.py"]])

    def test_file_below_minimum(self) -> None:
        '''a file smaller than the minimum returns an empty list'''
        self.assertEqual(find_large_files(self.h["hw3.py"], 8_001), [])

    def test_folder_high_threshold(self) -> None:
        '''a folder returns the large files from all nesting levels, in order'''
        expected = [self.h["resume.pdf"], self.h["lecture.mp4"], self.h["beach.jpg"]]
        self.assertEqual(find_large_files(self.h["home"], 100_000), expected)

    def test_folder_low_threshold(self) -> None:
        '''a lower threshold returns more files'''
        expected = [self.h["resume.pdf"], self.h["hw3.py"], self.h["lecture.mp4"], self.h["beach.jpg"]]
        self.assertEqual(find_large_files(self.h["home"], 5_000), expected)

    def test_zero_threshold_returns_all_files(self) -> None:
        '''a threshold of 0 returns every file and no folders'''
        result = find_large_files(self.h["home"], 0)
        self.assertEqual(len(result), 6)
        self.assertTrue(all(isinstance(f, File) for f in result))

    def test_subfolder(self) -> None:
        '''starting from a nested folder only searches that folder'''
        self.assertEqual(find_large_files(self.h["school"], 5_000), [self.h["hw3.py"], self.h["lecture.mp4"]])

    def test_threshold_above_everything(self) -> None:
        '''a threshold larger than every file returns an empty list'''
        self.assertEqual(find_large_files(self.h["home"], 10_000_000), [])

    def test_empty_folder(self) -> None:
        '''an empty folder returns an empty list'''
        self.assertEqual(find_large_files(self.h["empty"], 0), [])

    def test_plain_entry(self) -> None:
        '''a plain Entry has no files, so it returns an empty list'''
        self.assertEqual(find_large_files(Entry("plain"), 0), [])

    def test_negative_minimum(self) -> None:
        '''a negative minimum_size raises ValueError'''
        with self.assertRaises(ValueError):
            find_large_files(self.h["home"], -1)


class TestAbsolutePath(unittest.TestCase):
    '''unit tests for Entry.absolute_path()'''

    def setUp(self) -> None:
        '''builds a fresh hierarchy before every test'''
        self.h = build_hierarchy()

    def test_root(self) -> None:
        '''the root's path contains only the root'''
        self.assertEqual(self.h["home"].absolute_path(), [self.h["home"]])

    def test_file_in_root(self) -> None:
        '''a file directly in the root has a path of length 2'''
        self.assertEqual(self.h["readme.txt"].absolute_path(), [self.h["readme.txt"], self.h["home"]])

    def test_deepest_file(self) -> None:
        '''the deepest file's path goes through every folder up to the root'''
        h = self.h
        self.assertEqual(h["lecture.mp4"].absolute_path(), [h["lecture.mp4"], h["cop4045"], h["school"], h["docs"], h["home"]])

    def test_folder(self) -> None:
        '''absolute_path() also works on folders'''
        h = self.h
        self.assertEqual(h["empty"].absolute_path(), [h["empty"], h["pictures"], h["home"]])

    def test_starts_with_self_ends_with_root(self) -> None:
        '''every path starts with the entry itself and ends with the root'''
        for entry in self.h.values():
            path = entry.absolute_path()
            self.assertIs(path[0], entry)
            self.assertIs(path[-1], self.h["home"])
            self.assertIsNone(path[-1].parent())

    def test_entry_without_parent(self) -> None:
        '''an entry with no parent is its own root'''
        f = File("alone.txt", 10)
        self.assertEqual(f.absolute_path(), [f])

    def test_after_add(self) -> None:
        '''moving an entry with add() changes its path'''
        h = self.h
        h["pictures"].add(h["hw3.py"])
        self.assertEqual(h["hw3.py"].absolute_path(), [h["hw3.py"], h["pictures"], h["home"]])

def test_entry_file() -> None:
    '''testif function for Entry and File'''
    root = Entry("root")
    f1 = File("a.txt", 100, root)
    f2 = File("b.txt", 250, root)
    testif(root.parent() is None, "test root has no parent", "correct = None", "incorrect")
    testif(f1.parent() is root, "test file parent", "correct = " + f1.parent().name, "incorrect")
    testif(root.size() == 0, "test Entry size", "correct = " + str(root.size()), "incorrect")
    testif(f1.size() == 100, "test File size override", "correct = " + str(f1.size()), "incorrect")
    testif(total_size([root, f1, f2]) == 350, "test polymorphic total_size", "correct = " + str(total_size([root, f1, f2])), "incorrect")
    try:
        File("bad.txt", -5)
        testif(False, "test negative bytes_used", "", "no error raised")
    except ValueError:
        testif(True, "test negative bytes_used", "correct = ValueError raised")

def test_folder() -> None:
    '''testif function for Folder and absolute_path'''
    root = Folder("root")
    docs = Folder("docs", root) #added to root through the constructor
    a = File("a.txt", 100, docs)
    b = File("b.txt", 200)
    docs.add(b) #added through add()
    pics = Folder("pics")
    root.add(pics)
    c = File("c.png", 500, pics)
    empty = Folder("empty", root)
    testif(empty.size() == 0, "test empty folder size", "correct = " + str(empty.size()), "incorrect")
    testif(docs.size() == 300, "test folder size", "correct = " + str(docs.size()), "incorrect")
    testif(root.size() == 800, "test nested folder size", "correct = " + str(root.size()), "incorrect")
    testif(docs.children() == (a, b), "test children tuple", "correct = " + str([e.name for e in docs.children()]), "incorrect")
    testif(b.parent() is docs, "test add sets parent", "correct = " + b.parent().name, "incorrect")
    testif(root.absolute_path() == [root], "test root absolute_path", "correct = " + str(path_names(root)), "incorrect")
    testif(c.absolute_path() == [c, pics, root], "test nested absolute_path", "correct = " + str(path_names(c)), "incorrect")

def main() -> None:
    '''demonstrates polymorphism by processing Entry, File and Folder objects through the Entry interface'''
    root = Folder("root")
    docs = Folder("docs", root)
    notes = File("notes.txt", 1200, docs)
    photo = File("photo.png", 50000, root)
    entries: list[Entry] = [root, docs, notes, photo, Entry("plain")]
    for entry in entries:
        print(entry, "path:", path_names(entry)) #each object uses the size() of its own class
    print("Total size of root's children:", total_size(list(root.children())))
    test_entry_file()
    test_folder()
    demo_hierarchy() #parts f) and g)
    unittest.main(argv=["p6_Rutkis_Jorn"], verbosity=2, exit=False) #part e): runs all unit tests
    print("Jorn Rutkis")
    print("Z-Number: Z23737550")

if __name__ == "__main__":
    main()
