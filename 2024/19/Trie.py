import string
import unittest

class Trie:

    def __init__(self, alphabet=string.ascii_lowercase):
        self.alphabet = alphabet
        self.root = TrieNode(self.alphabet)

    def insert(self, word):
        current = self.root

        try:
            for c in word:
                if current.children[c] is None:
                    node = TrieNode(self.alphabet)
                    current.children[c] = node

                current = current.children[c]
        except KeyError:
            raise KeyError(f"Unexpected character '{c}' in '{word}'. Possible characters are {', '.join(self.alphabet.split())}")

        # Prevent the empty string from being considered a word
        current.is_word = len(word) > 0

    def remove(self, word):
        current = self.root
        last_common_node = None
        last_common_char = None

        try:
            for c in word:
                if current.children[c] is None:
                    return False

                if current.count_descendants() > 1:
                    last_common_node = current
                    last_common_char = c

                current = current.children[c]
        except KeyError:
            return False

        if current.is_word is False:
            return False

        if current.count_descendants() > 0:
            current.is_word = False
            return True

        if last_common_node is None:
            assert last_common_char is None
            self.root.children[word[0]] = None
        else:
            assert last_common_char is not None
            last_common_node.children[last_common_char] = None

        return True

    def find_prefix(self, prefix):
        current = self.root

        try:
            for c in prefix:
                if current.children[c] is None:
                    return False

                current = current.children[c]
        except KeyError:
            return False

        return True

    def find_word(self, word):
        current = self.root

        try:
            for c in word:
                if current.children[c] is None:
                    return False

                current = current.children[c]
        except KeyError:
            return False

        return current.is_word

class TrieNode:
    def __init__(self, alphabet):
        self.children = {char: None for char in alphabet}
        self.is_word = False

    def count_descendants(self):
        return sum([0 if n is None else 1 for n in self.children.values()])

class TestTrie(unittest.TestCase):
    def test_insertion_ok(self):
        tree = Trie()
        tree.insert("ant")

        self.assertTrue(tree.find_word("ant"), "Could not retrieve word from Trie")

    def test_insert_empty(self):
        tree = Trie()
        tree.insert("")

        self.assertFalse(tree.find_word(""), "Found unexpected word in Trie")

    def test_prefix(self):
        tree = Trie()
        tree.insert("dad")

        self.assertTrue(tree.find_prefix("d"), "Could not retrieve prefix from Trie")
        self.assertTrue(tree.find_prefix("da"), "Could not retrieve prefix from Trie")

        self.assertFalse(tree.find_prefix("ad"), "Found unexpected prefix in Trie")
        self.assertFalse(tree.find_prefix("dd"), "Found unexpected prefix in Trie")

    def test_word(self):
        tree = Trie()
        tree.insert("and")

        self.assertTrue(tree.find_word("and"), "Could not retrieve word from Trie")

        self.assertFalse(tree.find_word("an"), "Found unexpected word in Trie")
        self.assertFalse(tree.find_word("ad"), "Found unexpected word in Trie")
        self.assertFalse(tree.find_word("nd"), "Found unexpected word in Trie")
        self.assertFalse(tree.find_word("andy"), "Found unexpected word in Trie")

    def test_alphabet(self):
        tree = Trie("rgb")

        self.assertRaisesRegex(KeyError, "Unexpected character 'w'", tree.insert, "rgbw")
        self.assertRaisesRegex(KeyError, "Unexpected character 'w'", tree.insert, "rwgb")
        self.assertRaisesRegex(KeyError, "Unexpected character 'w'", tree.insert, "wrgb")

    def test_remove_lone_word(self):
        tree = Trie()

        tree.insert("ant")
        tree.insert("and")
        tree.insert("dad")

        self.assertTrue(tree.remove("dad"), "Could not remove existing word")

        self.assertFalse(tree.find_word("dad"), "Found unexpected word in Trie")
        self.assertFalse(tree.find_prefix("da"), "Found unexpected prefix in Trie")
        self.assertFalse(tree.find_prefix("d"), "Found unexpected prefix in Trie")

        self.assertTrue(tree.find_word("ant"), "Could not retrieve word from Trie")
        self.assertTrue(tree.find_word("and"), "Could not retrieve word from Trie")
        self.assertTrue(tree.find_prefix("an"), "Could not retrieve prefix from Trie")

    def test_remove_leaf_word(self):
        tree = Trie()

        tree.insert("ant")
        tree.insert("and")

        self.assertTrue(tree.remove("ant"), "Could not remove existing word")

        self.assertTrue(tree.find_word("and"), "Could not retrieve word from Trie")
        self.assertFalse(tree.find_word("ant"), "Found unexpected word in Trie")

    def test_remove_substring_word(self):
        tree = Trie()

        tree.insert("an")
        tree.insert("and")
        tree.insert("andy")

        self.assertTrue(tree.remove("and"), "Could not remove existing word")

        self.assertFalse(tree.find_word("and"), "Found unexpected word in Trie")
        self.assertTrue(tree.find_word("an"), "Could not retrieve word from Trie")
        self.assertTrue(tree.find_word("andy"), "Could not retrieve word from Trie")

    def test_remove_empty(self):
        tree = Trie()

        tree.insert("ant")

        self.assertFalse(tree.remove(""))
        self.assertTrue(tree.find_word("ant"), "Could not retrieve word from Trie")
