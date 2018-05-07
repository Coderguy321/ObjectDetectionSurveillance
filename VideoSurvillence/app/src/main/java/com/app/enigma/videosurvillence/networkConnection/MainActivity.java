package com.app.enigma.videosurvillence.networkConnection;

import android.os.AsyncTask;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.DefaultItemAnimator;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.widget.TextView;
import android.widget.Toast;

import com.app.enigma.videosurvillence.Adapter.CameraAdapter;
import com.app.enigma.videosurvillence.Model.Camera;
import com.app.enigma.videosurvillence.R;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    private List<Camera> cameraList = new ArrayList<>();
    private RecyclerView recyclerView;
    private CameraAdapter mAdapter;

    private Service mService;
    TextView testing;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        testing = (TextView)findViewById(R.id.textview);
        testing.setText("");

        recyclerView = (RecyclerView) findViewById(R.id.recycler_view);

        mAdapter = new CameraAdapter(cameraList);
        RecyclerView.LayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext());
        recyclerView.setLayoutManager(mLayoutManager);
        recyclerView.setItemAnimator(new DefaultItemAnimator());
        recyclerView.setAdapter(mAdapter);

//        if (API_KEY.isEmpty()) {
//            Toast.makeText(getApplicationContext(), "Please obtain your API KEY first from themoviedb.org", Toast.LENGTH_LONG).show();
//            return;
//        }











        mService = new Service();

        mService.getName(new ServiceCallback() {
            @Override
            public void onSuccess(AsyncTask.Status statusResponse, Object response) {

            }

            @Override
            public void onSuccess(Object response) {
                Snackbar.make(getCurrentFocus(),"Successfully synced", Snackbar.LENGTH_LONG);
                Toast.makeText(getApplicationContext(),"Successfully synced", Toast.LENGTH_LONG);
                android.util.Log.i("Response", response.toString());
            }

            @Override
            public void onFailure(Exception exception) {
                android.util.Log.e("Alert",exception.getMessage());
            }
        });


    }
















}
