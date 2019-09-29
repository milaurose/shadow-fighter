# shadow-fighter
This app applies Open Pose to simultaneously track the movements of two players, from two separate video feeds. 
The players can physically interact in a virtual space and play a boxing game, even if they are in separate rooms!
This was created for the ImplementAI 2019 Hackathon
INSERT PICTURE HERE

## Workflow
1. Broadcast video feeds from two separate cameras onto ngrok using a multi-threading approach.
2. Grab the frames from the video feeds and load them into Google Colab.
3. Display the pose estimates produced by Open Pose for both players on top of a common background made in OpenCV.
4. Each player can punch their opponent 'virtually' in order to decrease their opponent's health score.
INSERT WORKFLOW PICTURE HERE

## Plans for future improvements
* online deployment that allows users to connect via a website
* upgrade from Open Pose to wrnch API for more accurate tracking
* upgrade graphics in Unity

## Open Pose Arcade!
This method is really flexible and can be run on a standard laptop with no special equipment. 
We further demonstrated the flexibility by creating two-player physical versions of Atari and Pong, 
where each player controls their moves with physical movements instead of traditional key strokes.

## Built with
* Python 3+
* OpenCV
* Open Pose
* Tensorflow
* ngrok
* Google Colab

## References
* https://github.com/ildoonet/tf-pose-estimation
