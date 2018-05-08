package com.app.enigma.videosurvillence.Model;

import com.google.gson.annotations.SerializedName;

/**
 * Created by Jatinder Dhawan on 5/8/2018.
 */

public class CameraStatus {
    enum AlertStatus {
        RED_ALERT, OKAY
    }
    @SerializedName("cameraName")
    private String cameraName;

    @SerializedName("status")
    private AlertStatus status;

    public String getCameraName() {
        return cameraName;
    }

    public AlertStatus getStatus() {
        return this.status;
    }
}
