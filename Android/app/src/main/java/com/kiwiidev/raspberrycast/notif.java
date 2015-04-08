package com.kiwiidev.raspberrycast;

import android.app.IntentService;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Intent;
import android.graphics.BitmapFactory;
import android.support.v4.app.NotificationCompat;
import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;

import raspberrycast.kiwiidev.com.raspberrycast.R;


public class notif extends IntentService {

    private NotificationManager mNotificationManager;
    NotificationCompat.Builder builder;

    public notif() {
        // The super call is required. The background thread that IntentService
        // starts is labeled with the string argument you pass.
        super("raspberrycast.kiwiidev.com.raspberrycast");
    }

    @Override
    protected void onHandleIntent(Intent intent) {
        int result;
        URL target;
        Log.d("System.out","onHandleIntent has been called");
        NotificationManager nm = (NotificationManager)
                getSystemService(NOTIFICATION_SERVICE);

        String action = intent.getAction();
        // This section handles the possible actions:
        if(action.equals(CommonConstants.ACTION_START)){

            mNotificationManager = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
            Intent pauseIntent = new Intent(this, notif.class);
            pauseIntent.setAction(CommonConstants.ACTION_PAUSE);
            PendingIntent pipause = PendingIntent.getService(this, 0, pauseIntent, 0);

            Intent FFWIntent = new Intent(this, notif.class);
            FFWIntent.setAction(CommonConstants.ACTION_FAST_FORWARD);
            PendingIntent piFFW = PendingIntent.getService(this, 0, FFWIntent, 0);

            Intent revindIntent = new Intent(this, notif.class);
            revindIntent.setAction(CommonConstants.ACTION_REVIND);
            PendingIntent piRevind = PendingIntent.getService(this, 0, revindIntent, 0);

            // Constructs the Builder object.
            builder =
                    new NotificationCompat.Builder(this)
                            .setSmallIcon(R.drawable.notificon)
                            .setLargeIcon(BitmapFactory.decodeResource(getResources(), R.drawable.notification))
                            .setContentTitle("Remote")
//                          .setContentText("Pause")
//                          .setDefaults(Notification.DEFAULT_ALL)
                            .addAction(R.drawable.revind,
                                    "", piRevind)
                            .addAction(R.drawable.pause,
                                    "", pipause)
                            .addAction(R.drawable.ffw,
                                    "", piFFW);


            Intent resultIntent = new Intent(this, MainActivity.class);
            resultIntent.putExtra(CommonConstants.EXTRA_MESSAGE, "Started");
            resultIntent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);

            PendingIntent resultPendingIntent =
                    PendingIntent.getActivity(
                            this,
                            0,
                            resultIntent,
                            PendingIntent.FLAG_UPDATE_CURRENT
                    );

            builder.setContentIntent(resultPendingIntent);
            mNotificationManager.notify(CommonConstants.NOTIFICATION_ID, builder.build());

        }
        else if (action.equals(CommonConstants.ACTION_STOP)){
            nm.cancel(CommonConstants.NOTIFICATION_ID);
        }
        else if (action.equals(CommonConstants.ACTION_REVIND)){
            Log.d("System.out","ACTION_REVIND");
            target = null;
            try {
                target = new URL("http://" + CommonConstants.IP +":2020/video?control=pause");
                BufferedReader in = new BufferedReader(new InputStreamReader(target.openStream()));
                result = Integer.parseInt(in.readLine());
                in.close();
            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        else if(action.equals(CommonConstants.ACTION_PAUSE)) {
            Log.d("System.out","ACTION_PAUSE");
            target = null;
            try {
                target = new URL("http://" + CommonConstants.IP +":2020/video?control=pause");
                BufferedReader in = new BufferedReader(new InputStreamReader(target.openStream()));
                result = Integer.parseInt(in.readLine());
                in.close();
            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }

        } else if (action.equals(CommonConstants.ACTION_FAST_FORWARD)){
            Log.d("System.out","ACTION_FAST_FORWARD");
            target = null;
            try {
                target = new URL("http://" + CommonConstants.IP +":2020/video?control=right");
                BufferedReader in = new BufferedReader(new InputStreamReader(target.openStream()));
                result = Integer.parseInt(in.readLine());
                in.close();
            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
        } else if (action.equals(CommonConstants.ACTION_REVIND)) {
            Log.d("System.out", "ACTION_REVIND");
            target = null;
            try {
                target = new URL("http://" + CommonConstants.IP + ":2020/video?control=left");
                BufferedReader in = new BufferedReader(new InputStreamReader(target.openStream()));
                result = Integer.parseInt(in.readLine());
                in.close();
            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }


    private void issueNotification(NotificationCompat.Builder builder) {
        mNotificationManager = (NotificationManager)
                getSystemService(NOTIFICATION_SERVICE);
        // Including the notification ID allows you to update the notification later on.
        mNotificationManager.notify(CommonConstants.NOTIFICATION_ID, builder.build());
    }
}
