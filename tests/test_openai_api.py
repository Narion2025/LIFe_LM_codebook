import openai
import unittest

class TestOpenAISyntax(unittest.TestCase):
    def test_new_client(self):
        client = openai.OpenAI(api_key="sk-test")
        self.assertEqual(client.api_key, "sk-test")
        # ensure new style attributes are present
        self.assertTrue(hasattr(client, "models"))

if __name__ == "__main__":
    unittest.main()
