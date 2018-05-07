package com.app.enigma.videosurvillence.Adapter;

/**
 * Created by vishwasgarg on 08/05/18.
 */


import android.graphics.Color;
import android.graphics.drawable.AnimationDrawable;
import android.graphics.drawable.ColorDrawable;
import android.os.Handler;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import com.app.enigma.videosurvillence.Model.Camera;
import com.app.enigma.videosurvillence.Model.Log;
import com.app.enigma.videosurvillence.R;

import java.util.List;

public class CameraAdapter extends RecyclerView.Adapter<CameraAdapter.MyViewHolder> {

    private List<Camera> camerasList;
    public Button btn;
    public AnimationDrawable drawable;
    public Handler handler;

    public CameraAdapter(List<Camera> cameraList) {
        this.camerasList = cameraList;
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {
        public TextView title, year, genre;


        public MyViewHolder(View view) {
            super(view);
            title = (TextView) view.findViewById(R.id.title);

            drawable = new AnimationDrawable();
            handler = new Handler();

            drawable.addFrame(new ColorDrawable(Color.RED), 400);
            drawable.addFrame(new ColorDrawable(Color.GREEN), 400);
            drawable.setOneShot(false);
            btn = (Button)view.findViewById(R.id.button);


//            genre = (TextView) view.findViewById(R.id.genre);
//            year = (TextView) view.findViewById(R.id.year);
        }
    }


    @Override
    public MyViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.camera_row, parent, false);

        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(MyViewHolder holder, int position) {
        Camera camera = camerasList.get(position);
       // holder.title.setText("desfesf");
        holder.title.setText(camera.getTitle());
        btn.setBackgroundDrawable(drawable);
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                drawable.start();
            }
        }, 100);
    }

    @Override
    public int getItemCount() {
        return camerasList.size();
    }
}