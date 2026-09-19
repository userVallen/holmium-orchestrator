import os

from dotenv import load_dotenv

env_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.env.test"))
load_dotenv(env_test_path)
