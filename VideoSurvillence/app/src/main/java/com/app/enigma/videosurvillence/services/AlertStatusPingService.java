package com.app.enigma.videosurvillence.services;

import android.app.IntentService;
import android.content.Intent;
import android.content.Context;

import com.app.enigma.videosurvillence.networkConnection.RetrofitBuilder;
import com.app.enigma.videosurvillence.networkConnection.Service;

import retrofit2.Retrofit;

public class AlertStatusPingService extends IntentService {

    public AlertStatusPingService() {
        super("AlertStatusPingService");
    }

    @Override
    protected void onHandleIntent(Intent intent) {
        System.out.println("Initiating service");
        if (intent != null) {
            while (true) {
                try {
                    System.out.println("alert status");
                    new Service().pingAlertStatus();
                    Thread.sleep(5000);
                } catch (InterruptedException exception) {
                    exception.printStackTrace();
                }
            }
        }
        throw new RuntimeException("Cannot start service");
    }
}
