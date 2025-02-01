from sensor.exception import SensorException,sys
from sensor.logger import logging


def test_execution():
    
    try:
        a=110
        logging.info('Error check at main module {}'.format(a))
        a/0
    except Exception as e:
        raise SensorException(e,sys)
        


if __name__ == '__main__':  #it will run progm on only this page other import will restrict
    
    try:
        test_execution()
    except SensorException as e:
        print(e)
    



