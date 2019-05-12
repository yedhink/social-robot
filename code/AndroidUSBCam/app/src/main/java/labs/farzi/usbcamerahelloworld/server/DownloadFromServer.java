package miniproj.ikigai.usbcamerahelloworld.server;

import android.content.Context;
import android.util.Log;
import android.widget.Toast;


import net.gotev.speech.Speech;

import miniproj.ikigai.usbcamerahelloworld.apis.RetrofitDownloadImage;
import miniproj.ikigai.usbcamerahelloworld.voices.Talking;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

import static miniproj.ikigai.usbcamerahelloworld.MainActivity.URL;
import static miniproj.ikigai.usbcamerahelloworld.voices.Talking.speak;

public class DownloadFromServer {


	static void getRetrofitImage(final Context context, String cookie) {
		Retrofit retrofit = new Retrofit.Builder()
			                    .baseUrl(URL)
			                    .addConverterFactory(GsonConverterFactory.create())
			                    .build();
		RetrofitDownloadImage service = retrofit.create(RetrofitDownloadImage.class);
		Call<ResponseBody> call = service.getImageDetails(cookie);
		call.enqueue(new Callback<ResponseBody>() {
			@Override
			public void onResponse(Call<ResponseBody> call, Response<ResponseBody> response) {
				try {
					Log.d("onResponse", "Response came from server");
					String pred = response.body().string();
					Log.e("PREDICTION2", "onResponse: prediction = " + pred);

					Toast.makeText(context, pred,
						Toast.LENGTH_SHORT).show();

					// Speak out the prediction
					speak(pred.toLowerCase());

				} catch (Exception e) {
					Log.d("onResponse", "There is an error");
					e.printStackTrace();
				}
			}

			@Override
			public void onFailure(Call<ResponseBody> call, Throwable t) {
				Log.d("onFailure", t.toString());
			}

			public void onResponseBody(Response<ResponseBody> response, Retrofit retrofit) {
				try {
					Log.e("onResponse", "Response came from server in SECOND");
				} catch (Exception e) {
					Log.d("onResponse", "There is an error");
					e.printStackTrace();
				}
			}

			public void onFailure(Throwable t) {
				Log.d("onFailure", t.toString());
			}
		});
	}
}
