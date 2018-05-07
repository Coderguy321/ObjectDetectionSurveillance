package com.app.enigma.videosurvillence.networkConnection;

import android.os.AsyncTask;

/**
 * Created by abc on 13-09-2017.
 */

public interface ServiceCallback<T> {
    void onSuccess(AsyncTask.Status statusResponse, T response);
    void onSuccess(T response);
    void onFailure(Exception exception);
}
