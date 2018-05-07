package com.app.enigma.videosurvillence.Adapter;

/**
 * Created by vishwasgarg on 08/05/18.
 */


import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.app.enigma.videosurvillence.Model.Camera;
import com.app.enigma.videosurvillence.Model.Log;

import java.util.List;

public class CameraAdapter extends RecyclerView.Adapter<CameraAdapter.MyViewHolder> {

    private List<Camera> camerasList;

    public class MyViewHolder extends RecyclerView.ViewHolder {
        public TextView title, year, genre;

        public MyViewHolder(View view) {
            super(view);
//            title = (TextView) view.findViewById(R.id.title);
//            genre = (TextView) view.findViewById(R.id.genre);
//            year = (TextView) view.findViewById(R.id.year);
        }
    }


    public void CamerasAdpater(List<Camera> camerasList) {
        this.camerasList = camerasList;
    }

    @Override
    public MyViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.movie_list_row, parent, false);

        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(MyViewHolder holder, int position) {
        Camera camera = camerasList.get(position);
        //holder.title.setText(camera.getTitle());
    }

    @Override
    public int getItemCount() {
        return camerasList.size();
    }
}