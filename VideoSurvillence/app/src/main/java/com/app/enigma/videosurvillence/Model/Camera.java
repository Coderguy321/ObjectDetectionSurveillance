package com.app.enigma.videosurvillence.Model;

/**
 * Created by vishwasgarg on 08/05/18.
 */

public class Camera {
    private String title;

    public Camera(String title) {
        this.title = title;
    }

    public String getTitle(){
        return this.title;
    }

    public void setTitle(String title){
        this.title = title;
    }
}
