# GymLytics 🏋️

Visual Analytics of different exercises for humans with real-time coaching feedback

## Features ✨

- **Real-time exercise analysis** using computer vision
- **Audio coaching feedback** - voice alerts when form is incorrect
- **Multi-exercise support** with pose detection
- **Visual form scoring** with accuracy percentages
- **Webcam and video file support**
- **Instant feedback system** for proper form correction

## Code Requirements 🦄

You can install Conda for python which resolves all the dependencies for machine learning.

```bash
pip install -r requirements.txt
```

## Description 🏃

Exercise is any bodily activity that enhances or maintains physical fitness and overall health and wellness. It is performed for various reasons, to aid growth and improve strength, preventing aging, developing muscles and the cardiovascular system, honing athletic skills, weight loss or maintenance, improving health and also for enjoyment. Many individuals choose to exercise outdoors where they can congregate in groups, socialize, and enhance well-being.

**GymLytics** takes your workout experience to the next level by providing real-time visual analytics and audio coaching feedback. The system monitors your exercise form and provides instant corrections through voice alerts, helping you maintain proper technique and maximize your workout effectiveness.

## Python Implementation 👨‍🔬

### Supported Exercise Types
- **Pushup** - Upper body strength training
- **Squat** - Lower body and core strengthening
- **Lunges** - Leg and glute development
- **Shoulder Taps** - Core stability and shoulder strength
- **Plank** - Core endurance and stability

### Audio Coaching System 🔊
The integrated coach provides real-time audio feedback:
- **Form correction alerts** - "Adjust your posture" when technique is off
- **Motivational cues** - "Great form, keep it up!" for proper execution
- **Count announcements** - Rep counting with voice confirmation
- **Position guidance** - Specific instructions for body alignment

### Source Options
- `'0'` for webcam (real-time analysis)
- Any video file path for pre-recorded exercise analysis

If you face any problem, kindly raise an issue

## Setup 🖥️

### Prerequisites
- Python 3.7+
- Webcam (for real-time analysis)
- Audio output device (for coaching feedback)

### Installation Steps
1. Clone the repository
```bash
git clone https://github.com/yourusername/GymLytics.git
cd GymLytics
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up your exercise environment:
   - Position camera to capture full body
   - Ensure good lighting conditions
   - Test audio output for coaching feedback

### Configuration
1. Record the exercise you want to perform analytics on; or set up your webcam for real-time streaming
2. Select the type of exercise you want to perform (see supported exercises above)
3. Ensure audio is enabled for coaching feedback
4. Run the `GymLytics.py` file with your desired configuration

## Execution 🐉

### Basic Usage
```bash
python3 GymLytics.py --type pushup --source 0
```

### Video File Analysis
```bash
python3 GymLytics.py --type pushup --source resources/push_aks.mov
```

### Advanced Options
```bash
# With coaching feedback disabled
python3 GymLytics.py --type squat --source 0 --no-audio

# Custom confidence threshold
python3 GymLytics.py --type plank --source 0 --confidence 0.8

# Save analysis results
python3 GymLytics.py --type lunges --source workout_video.mp4 --save-results
```

## Audio Coaching Features 🎯

### Real-time Form Correction
- **Posture Alerts**: "Keep your back straight" for planks and pushups
- **Depth Guidance**: "Go lower" for squats and lunges
- **Alignment Cues**: "Center your weight" for balance exercises

### Motivational Feedback
- **Progress Tracking**: "Rep 15 completed, excellent form!"
- **Encouragement**: "You're doing great, maintain that position"
- **Achievement Milestones**: "New personal best - 30 perfect pushups!"

### Customizable Voice Settings
- Adjustable volume levels
- Multiple voice options (male/female)
- Language support (English, Spanish, French)
- Coaching intensity levels (gentle, standard, intense)

## Results 📊

### Push ups
<div align="center">
<img src="https://github.com/akshaybahadur21/BLOB/blob/master/push.gif" width=800>
</div>

*Real-time pushup analysis with form scoring and audio coaching feedback*

### Squats  
<div align="center">
<img src="https://github.com/akshaybahadur21/BLOB/blob/master/gym_squats.gif" width=400>
</div>

*Squat depth analysis with voice guidance for proper technique*

## Performance Metrics 📈

The system provides detailed analytics including:
- **Form Accuracy Score** (0-100%)
- **Rep Count** with validity verification
- **Time Under Tension** for each exercise
- **Improvement Tracking** over sessions
- **Common Mistakes** identification and correction

## Troubleshooting 🔧

### Common Issues
- **No audio feedback**: Check system volume and audio device settings
- **Poor pose detection**: Ensure adequate lighting and full body visibility
- **False coaching alerts**: Adjust confidence threshold in settings

### Performance Optimization
- Use good lighting for better pose detection
- Position camera at chest level for optimal angle
- Ensure stable internet connection for real-time processing

## Contributing 🤝

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- MediaPipe for pose detection capabilities
- OpenCV community for computer vision tools
- Contributors who helped improve the coaching algorithms

---

**Ready to revolutionize your workout? Start your fitness journey with GymLytics today! 💪**
