
import numpy as np

import vision_coin



def main():

    roi_coords = np.array([[323, 472], [243, 411]]) # [[411, 243], [472, 323]] for coin_test_1.mp4
    results = vision_coin.run(3, roi_coords)


    return 1



if __name__ == "__main__":
    # execute only if run as a script
    main()