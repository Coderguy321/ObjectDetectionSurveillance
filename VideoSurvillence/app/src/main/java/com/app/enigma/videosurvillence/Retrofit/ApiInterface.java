package com.app.enigma.videosurvillence.Retrofit;

/**
 * Created by vishwasgarg on 07/05/18.
 */

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Path;
import retrofit2.http.Query;
import com.app.enigma.videosurvillence.Model.Log;

public interface ApiInterface {
    @GET("movie/top_rated")
    Call<Log> getTopRatedMovies(@Query("api_key") String apiKey);

//    @GET("movie/{id}")
//    Call<MoviesResponse> getMovieDetails(@Path("id") int id, @Query("api_key") String apiKey);

}
