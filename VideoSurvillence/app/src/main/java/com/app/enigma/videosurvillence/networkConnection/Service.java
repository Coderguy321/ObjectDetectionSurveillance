package com.app.enigma.videosurvillence.networkConnection;
import com.google.gson.JsonObject;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import com.app.enigma.videosurvillence.Model.Log;

/**
 * Created by abc on 13-09-2017.
 */

public class Service {

    public final String BASE_URL = "http://172.31.78.10:8000/";/*ec2-52-15-178-137.us-east-2.compute.amazonaws.com/*/

//    public void sendPost(StatsRequest statsRequest, final ServiceCallback serviceCallback) {


    public void getName(final ServiceCallback serviceCallback) {
        Retrofit retrofit = RetrofitBuilder
                .with()
                .baseUrl(BASE_URL)
                .build();
        //Post post = new Post(username, password);
        Apis.getLogName logName = (retrofit.create(Apis.getLogName.class));
        Call<com.app.enigma.videosurvillence.Model.Log> call = logName.getLogName();
        call.enqueue(new Callback<com.app.enigma.videosurvillence.Model.Log>() {

            @Override
            public void onResponse(Call<com.app.enigma.videosurvillence.Model.Log> call, Response<com.app.enigma.videosurvillence.Model.Log> response) {
                if (response.isSuccessful()) {
                    serviceCallback.onSuccess(response.body().toString());
                } else {
                    android.util.Log.d("Response received: ", "Authorization failure");
                }
            }

            @Override
            public void onFailure(Call<com.app.enigma.videosurvillence.Model.Log> call, Throwable t) {
                android.util.Log.e("onFailure", t.getMessage());
            }
        });
    }

}
