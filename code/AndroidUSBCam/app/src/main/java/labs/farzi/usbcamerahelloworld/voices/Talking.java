package miniproj.ikigai.usbcamerahelloworld.voices;

import net.gotev.speech.Speech;

public class Talking {

	public static void speak(String pred){
		Speech.getInstance().say(pred);
	}
}
