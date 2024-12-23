Hand Tracking and Gesture-Controlled Volume Adjustment

This repository contains two main components:
	1.	A Hand Tracking Module built using Mediapipe and OpenCV for real-time hand detection and landmark tracking.
	2.	A Volume Control Application that leverages hand gestures to control the system’s audio volume, utilizing the pycaw library.

Features

Hand Tracking Module
	•	Detect hands and draw landmarks using a webcam.
	•	Identify the positions of 21 hand landmarks.
	•	Determine which fingers are up and calculate distances between key landmarks.

Volume Control Application
	•	Adjust system volume based on the distance between the thumb and index finger.
	•	Visual feedback with a volume bar and percentage display.
	•	High FPS for smooth real-time interaction.
