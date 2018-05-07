package com.app.enigma.videosurvillence.networkConnection;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.io.IOException;
import java.util.concurrent.TimeUnit;

import okhttp3.Interceptor;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.logging.HttpLoggingInterceptor;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

/**
 * Created by kirandeep on 13-09-2017.
 */

public class RetrofitBuilder {
    private Retrofit.Builder builder;
    private static String auth;
    private static RetrofitBuilder instance;

    private RetrofitBuilder(){
        Gson gson = new GsonBuilder()
                .setDateFormat("yyyy-MM-dd'T'HH:mm:ssZ")
                .create();

        HttpLoggingInterceptor loggingInterceptor = new HttpLoggingInterceptor();
        loggingInterceptor.setLevel(HttpLoggingInterceptor.Level.BODY);

        OkHttpClient httpClient = new OkHttpClient.Builder()
                .addInterceptor(new Interceptor() {
                    @Override
                    public Response intercept(Chain chain) throws IOException {
                        Request.Builder builder = chain.request().newBuilder();
                        //builder.addHeader("Authorization", getAuth());
                        //builder.addHeader("Authorization", "Basic Ytpi");
                        builder.addHeader("Accept", "application/json");
                        Request request = builder.build();
                        return chain.proceed(request);
                    }
                })
                .readTimeout(60, TimeUnit.SECONDS)
                .connectTimeout(60, TimeUnit.SECONDS)
                .addInterceptor(loggingInterceptor)
                .build();

        builder = new Retrofit.Builder();
        builder.client(httpClient);
        builder.addConverterFactory(GsonConverterFactory.create(gson));
    }

    public static RetrofitBuilder with(){
        if(instance == null){
            instance = new RetrofitBuilder();
        }
        return instance;
    }

    public RetrofitBuilder baseUrl(String baseUrl){
        this.builder.baseUrl(baseUrl);
        return this;
    }

    public Retrofit build(){
        return this.builder.build();
    }

    /*private static String getAuth(){
        if(auth == null) {
            return Credentials.basic(BuildConfig.serviceUsername, BuildConfig.servicePassword);
        }
        return auth;
    }*/

    public static void setAuth(String authToken) {
        auth = authToken;
    }
}
