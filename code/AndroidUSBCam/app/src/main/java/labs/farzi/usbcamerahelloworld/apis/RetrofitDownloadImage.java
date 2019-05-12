package miniproj.ikigai.usbcamerahelloworld.apis;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Query;

public interface RetrofitDownloadImage {
	@GET("/download")
	Call<ResponseBody> getImageDetails(@Query("cookie") String cookie);
}
