package miniproj.ikigai.usbcamerahelloworld.apis;


import okhttp3.MultipartBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;

public interface RetrofitInterface {
	@Multipart
//	@Headers("Content-Type: text/html; charset=UTF-8")
	@POST("/upload")
	Call<ResponseBody> uploadImage(@Part MultipartBody.Part image);
}
