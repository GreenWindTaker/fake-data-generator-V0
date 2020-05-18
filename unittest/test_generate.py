import sys
import os

__home_dir = (os.path.dirname(os.path.dirname(__file__)))
print(str(__home_dir))
sys.path.append(__home_dir)


from service.fake_data_generator import FakeDataGenerator

def __test_generate():
    print("Generate Test")

    mfdg = FakeDataGenerator(isDebug=True)
    mfdg.loading_fake_data(${"TEST_API_KEY"})
    mfdg.generate_fake_body()
    mfdg.save_to_pandas()

__test_generate()