package miniproj.ikigai.usbcamerahelloworld.server;

import android.content.Context;
import android.util.Log;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonSyntaxException;
import miniproj.ikigai.usbcamerahelloworld.apis.RetrofitInterface;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

import static miniproj.ikigai.usbcamerahelloworld.MainActivity.URL;
import static miniproj.ikigai.usbcamerahelloworld.server.DownloadFromServer.getRetrofitImage;

public class UploadToServer {


	public static void uploadImage(final Context context, byte[] imageBytes, final String cookie) {
		Log.e("UPLOAD", "Entered upload image");
		Gson gson = new GsonBuilder()
			            .setLenient()
			            .create();

		Retrofit retrofit = new Retrofit.Builder()
			                    .baseUrl(URL)
			                    .addConverterFactory(GsonConverterFactory.create(gson))
			                    .build();

		RetrofitInterface retrofitInterface = retrofit.create(RetrofitInterface.class);

		try {
			RequestBody requestFile = RequestBody.create(MediaType.parse("image/jpeg"), imageBytes);
			MultipartBody.Part body = MultipartBody.Part.createFormData("image", cookie + ".jpg", requestFile);
			Call<ResponseBody> call = retrofitInterface.uploadImage(body);
			call.enqueue(new Callback<ResponseBody>() {
				@Override
				public void onResponse(Call<ResponseBody> call, Response<ResponseBody> response) {
					Log.e("SUCCESUPLOAD", response.message());
					getRetrofitImage(context,cookie);
				}

				@Override
				public void onFailure(Call<ResponseBody> call, Throwable t) {
				}
			});
		} catch (IllegalStateException | JsonSyntaxException exception) {
			Log.e("JSON", exception.getLocalizedMessage());
		}
	}
}
