package com.app.enigma.videosurvillence.networkConnection;

import android.graphics.Color;
import android.graphics.drawable.AnimationDrawable;
import android.graphics.drawable.ColorDrawable;
import android.media.AudioManager;
import android.media.Ringtone;
import android.media.RingtoneManager;
import android.media.ToneGenerator;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Handler;
import android.support.annotation.RequiresApi;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.DefaultItemAnimator;
import android.support.v7.widget.DividerItemDecoration;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.PopupWindow;
import android.widget.TextView;
import android.widget.Toast;

import com.app.enigma.videosurvillence.Adapter.CameraAdapter;
import com.app.enigma.videosurvillence.Adapter.RecyclerTouchListener;
import com.app.enigma.videosurvillence.Model.Camera;
import com.app.enigma.videosurvillence.R;

import java.util.ArrayList;
import java.util.List;

import static android.support.v7.recyclerview.R.styleable.RecyclerView;

public class MainActivity extends AppCompatActivity {

    private List<Camera> cameraList = new ArrayList<>();
    private RecyclerView recyclerView;
    private CameraAdapter mAdapter;
    Button showPopupBtn, closePopupBtn;
    PopupWindow popupWindow;
    LinearLayout linearLayout1;
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
        recyclerView.addOnItemTouchListener(new RecyclerTouchListener(getApplicationContext(), recyclerView, new RecyclerTouchListener.ClickListener() {
            @Override
            public void onClick(View view, int position) {
                Camera movie = cameraList.get(position);
                Toast.makeText(getApplicationContext(), movie.getTitle() + " is selected!", Toast.LENGTH_SHORT).show();


                //instantiate the popup.xml layout file
                LayoutInflater layoutInflater = (LayoutInflater) getApplicationContext() .getSystemService(getApplicationContext() .LAYOUT_INFLATER_SERVICE);
                View customView = layoutInflater.inflate(R.layout.popup_alert,null);

                //closePopupBtn = (Button) customView.findViewById(R.id.closePopupBtn);

                //instantiate popup window
                popupWindow = new PopupWindow(customView, android.support.v7.widget.RecyclerView.LayoutParams.WRAP_CONTENT, android.support.v7.widget.RecyclerView.LayoutParams.WRAP_CONTENT);

                //display the popup window
                popupWindow.showAtLocation(linearLayout1, Gravity.CENTER, 0, 0);

                //close the popup window on button click
//                closePopupBtn.setOnClickListener(new View.OnClickListener() {
//                    @Override
//                    public void onClick(View v) {
//                        popupWindow.dismiss();
//                    }
//                });
            }

            @Override
            public void onLongClick(View view, int position) {

            }
        }));





        ToneGenerator toneG = new ToneGenerator(AudioManager.STREAM_ALARM, 100000);
        toneG.startTone(ToneGenerator.TONE_CDMA_ALERT_CALL_GUARD, 1600000);

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
