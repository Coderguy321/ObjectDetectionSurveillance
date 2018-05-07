package com.app.enigma.videosurvillence.networkConnection;

import com.app.enigma.videosurvillence.Model.Log;
import com.google.gson.JsonObject;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;

/**
 * Created by abc on 13-09-2017.
 */

public interface Apis {
    interface getLogName {
        @GET("surveillance/name/")
        Call<Log> getLogName();
    }
}
