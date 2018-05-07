package com.app.enigma.videosurvillence;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

import com.app.enigma.videosurvillence.Model.Log;
import com.app.enigma.videosurvillence.Retrofit.ApiClient;
import com.app.enigma.videosurvillence.Retrofit.ApiInterface;

import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity {

    TextView testing;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        testing = (TextView)findViewById(R.id.textview);
        testing.setText("");

//        if (API_KEY.isEmpty()) {
//            Toast.makeText(getApplicationContext(), "Please obtain your API KEY first from themoviedb.org", Toast.LENGTH_LONG).show();
//            return;
//        }

        ApiInterface apiService =
                ApiClient.getClient().create(ApiInterface.class);

        Call<Log> call = apiService.getLogName();
        call.enqueue(new Callback<Log>() {
            @Override
            public void onResponse(Call<Log>call, Response<Log> response) {
                String Name = response.body().getName();
                testing.setText(Name);
                android.util.Log.d("Name of Log", Name);
            }

            @Override
            public void onFailure(Call<Log> call, Throwable t) {
                // Log error here since request failed
//                android.util.Log.e(TAG, t.toString());
            }
        });
    }
}
