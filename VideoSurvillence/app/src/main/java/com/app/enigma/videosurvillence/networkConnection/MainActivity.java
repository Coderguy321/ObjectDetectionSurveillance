package com.app.enigma.videosurvillence.networkConnection;

import android.content.Intent;
import android.media.AudioManager;
import android.media.Ringtone;
import android.media.RingtoneManager;
import android.media.ToneGenerator;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Build;
import android.support.annotation.RequiresApi;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.DefaultItemAnimator;
import android.support.v7.widget.DividerItemDecoration;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.widget.TextView;
import android.widget.Toast;

import com.app.enigma.videosurvillence.Adapter.CameraAdapter;
import com.app.enigma.videosurvillence.Model.Camera;
import com.app.enigma.videosurvillence.R;
import com.app.enigma.videosurvillence.services.AlertStatusPingService;

import java.util.ArrayList;
import java.util.List;

import static android.support.v7.recyclerview.R.styleable.RecyclerView;

public class MainActivity extends AppCompatActivity {

    private List<Camera> cameraList = new ArrayList<>();
    private RecyclerView recyclerView;
    private CameraAdapter mAdapter;

    private Service mService;
    TextView testing;

    @RequiresApi(api = Build.VERSION_CODES.GINGERBREAD)
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
        recyclerView.addItemDecoration(new DividerItemDecoration(this, LinearLayoutManager.VERTICAL));
        recyclerView.setAdapter(mAdapter);

        System.out.println("Triggering service");
        startService(new Intent(this, AlertStatusPingService.class));
//        ToneGenerator toneGen1 = new ToneGenerator(AudioManager.STREAM_MUSIC, 1000000000);
//        toneGen1.startTone(ToneGenerator.TONE_CDMA_PIP,10000000);

        ToneGenerator toneG = new ToneGenerator(AudioManager.STREAM_ALARM, 100000);
        toneG.startTone(ToneGenerator.TONE_CDMA_ALERT_CALL_GUARD, 1600000);


//        try {
//            Uri notification = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);
//            Ringtone r = RingtoneManager.getRingtone(getApplicationContext(), notification);
//            r.play();
//        } catch (Exception e) {
//            e.printStackTrace();
//        }
        prepareDummyCameraData();

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



    public void prepareDummyCameraData(){
        Camera camera1 = new Camera("CSE dept Camera");
        Camera camera2 = new Camera("Metta Parking Camera");
        cameraList.add(camera1);
        cameraList.add(camera2);

    }

}
