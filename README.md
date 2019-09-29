# shadow-fighter
This app applies Open Pose to simultaneously track the movements of two players, from two separate video feeds. 
The players can physically interact in a virtual space and play a boxing game, even if they are in separate rooms!
This was created for the ImplementAI 2019 Hackathon.

## Open Pose Arcade!
This method is really flexible and can be run on a standard laptop with no special equipment. We further demonstrated the flexibility by creating two-player physical versions of Atari and Pong, where each player controls their moves with physical movements instead of traditional key strokes. This brings back retro games with a new interactive twist that transforms sedentary individual games into collaborative exercise.

[Demo: Stand-alone web Atari Breakout using posenet for controls](https://atari-posenet.firebaseapp.com)

## Workflow
1. Local clients uses Flask to broadcast each player's video feeds on the local area network via a multi-threaded video capture class.
2. Use ngrok port forwarding to make each video feed public accessible
3. Pose estimation server hosted on Google Colab accesses the video feeds
4. Server estimates joint landmark vector for each player via a modified Open Pose model.
5. Server streams back joint vectors via Flask and additional ngrok tunneling
6. Local client processes joint vectors and reconstruct skeletal representation of each player in a common virtual space
7. Further movement analysis and interaction leads to abilities such as virtual boxing matches and pose mimcking

## Plans for future improvements
* online deployment that allows users to connect via a website and removes need for local client
* upgrade from Open Pose to wrnch API for more accurate tracking (especially occluded joints) for estimating more complex player dynamics
* upgrade graphics to Unity Game Engine (3D characters, realistic textures etc)

## Built with
* Python 3+
* OpenCV
* Open Pose
* Tensorflow
* ngrok
* Google Colab
* Flask

## References
* https://github.com/ildoonet/tf-pose-estimation
* https://blog.miguelgrinberg.com/post/video-streaming-with-flask
* https://imadelhanafi.com/posts/google_colal_server/
