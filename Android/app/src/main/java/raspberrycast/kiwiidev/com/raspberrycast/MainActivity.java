package raspberrycast.kiwiidev.com.raspberrycast;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.IntentService;
import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Bundle;
import android.support.v4.app.NotificationCompat;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.EditText;
import android.widget.RemoteViews;
import android.widget.Toast;

import java.net.URL;


public class MainActivity extends Activity {

    private String  url="";
    private String ip ="";
    private String IPsettings = "settings";
    final String notavailable = "<html><title>Server name not Valid</title><body><h2>The IP Address is not Valid</h2><p>The IP Address is invalid or not entered at all</p><p>If you have not set it yet, please <b>Set the IP Address of your Raspberry Pi</b></p></body></html>";
    private Intent mServiceIntent;
    NotificationCompat.Builder builder;
    private NotificationManager mNotificationManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Log.d("MAIN", "OnCreated");
        SharedPreferences settings = getSharedPreferences(getIPsettings(),MODE_PRIVATE);
        setIp(settings.getString(IPsettings,"Not Available"));
        ip = settings.getString(getIPsettings(), "Not Available");

        setUrl("http://" + getIp() + ":2020/remote");
        WebView remote = (WebView) findViewById(R.id.remote);

        remote = (WebView) findViewById(R.id.remote);
        remote.setVerticalScrollBarEnabled(true);
        remote.setHorizontalScrollbarOverlay(true);
        remote.getSettings().setJavaScriptEnabled(true);

        CommonConstants.IP = getIp();

        if(!getIp().equals("Not Available")) {

            remote.loadUrl(getUrl());
            Log.d("WebView", "Loading Site");
            super.onCreate(savedInstanceState);
            final Activity activity = this;
            remote.setWebViewClient(new WebViewClient() {
                public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
                    Toast.makeText(activity, description, Toast.LENGTH_SHORT).show();
                }
            });
            final WebView finalRemote = remote;
            remote.setWebViewClient(new WebViewClient() {
                @Override
                public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
                    Log.d("WebView", "Not found");
                    finalRemote.loadData(notavailable, "text/html", null);
                    setIPAddress();
                }
            });
        }
        else if(getIp().equals("Not Available") || getIp().contains("\n")){
            setIPAddress();
            Log.d("WebView","Not Available");
            remote.loadData(notavailable, "text/html", null);}

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        final Context context = this;
        final SharedPreferences settings = getSharedPreferences(getIPsettings(),MODE_PRIVATE);
        final SharedPreferences.Editor PrefEditor = settings.edit();
        final WebView remote = (WebView) findViewById(R.id.remote);

        switch (item.getItemId()) {
            case R.id.action_settings:
                LayoutInflater li = LayoutInflater.from(context);
                View promptsView = li.inflate(R.layout.activity_settings, null);
                AlertDialog.Builder alertDialogBuilder = new AlertDialog.Builder(context);
                alertDialogBuilder.setView(promptsView);
                final EditText userInput = (EditText) promptsView.findViewById(R.id.editTextDialogUserInput);
                alertDialogBuilder.setCancelable(false).setPositiveButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialogInterface, int i) {
                        PrefEditor.putString(getIPsettings(), userInput.getText().toString());
                        PrefEditor.commit();

                        setIp(settings.getString(getIPsettings(), "Not Available"));
                        setUrl("http://" + getIp() + ":2020/remote");
                        if(getIp() != "Not Available" ) {
                            remote.loadUrl(url);
                        }
                        else {
                            setIPAddress();
                            Log.d("WebView","Not Available");
                            remote.loadData(notavailable, "text/html", null);
                        }
                    }
                })
                        .setNegativeButton("Cancel",new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialogInterface, int i) {
                                dialogInterface.cancel();
                            }
                        });

                AlertDialog alertDialog = alertDialogBuilder.create();
                alertDialog.show();

                //setContentView(R.layout.activity_settings);
                return true;
            case R.id.refresh:
                remote.loadData("<html><h1>REFRESHING</h1><p>Please wait while the page loads</p></html>","text/html",null);
                remote.loadUrl(getUrl());
                return true;
            case R.id.about:
                Intent browserIntent = new Intent(Intent.ACTION_VIEW, Uri.parse("https://github.com/vincent-lwt/RaspberryCast"));
                startActivity(browserIntent);
                return true;
            case R.id.notification:
                if(item.isChecked()){
                    setNotificationStatus(false);
                    item.setChecked(false);
                }
                else if(!item.isChecked()){
                    item.setChecked(true);
                    setNotificationStatus(true);
                }
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }

        //return super.onOptionsItemSelected(item);
    }
    public String getUrl() {
        return url;
    }public void setUrl(String url) {
        this.url = url;
    }public String getIp() {
        return ip;
    }public void setIp(String ip) {
        this.ip = ip;
    }public String getIPsettings() {
        return IPsettings;
    }public void setIPsettings(String IPsettings) {
        this.IPsettings = IPsettings;
    }

    public void setIPAddress(){
        Log.d("SetIPAddress","Setting using popup menu");
        final Context context = this;
        final SharedPreferences settings = getSharedPreferences(getIPsettings(),MODE_PRIVATE);
        final SharedPreferences.Editor PrefEditor = settings.edit();
        final WebView remote = (WebView) findViewById(R.id.remote);
        LayoutInflater li = LayoutInflater.from(context);
        View promptsView = li.inflate(R.layout.activity_settings, null);
        AlertDialog.Builder alertDialogBuilder = new AlertDialog.Builder(context);
        alertDialogBuilder.setView(promptsView);
        final EditText userInput = (EditText) promptsView.findViewById(R.id.editTextDialogUserInput);
        alertDialogBuilder.setCancelable(false).setPositiveButton("OK", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                PrefEditor.putString(getIPsettings(), userInput.getText().toString());
                PrefEditor.commit();

                setIp(settings.getString(getIPsettings(), "Not Available"));
                setUrl("http://" + getIp() + ":2020/remote");
                remote.loadUrl(url);
            }
        })
                .setNegativeButton("Cancel",new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialogInterface, int i) {
                        dialogInterface.cancel();
                    }
                });

        AlertDialog alertDialog = alertDialogBuilder.create();
        alertDialog.show();
    }

    public void setNotificationStatus(boolean stats){

        Log.d("System.out","Notification initialising");

        mServiceIntent = new Intent(getApplicationContext(), notif.class);
        mServiceIntent.setAction(CommonConstants.ACTION_START);
        mServiceIntent.putExtra(CommonConstants.IP,getIp());

        startService(mServiceIntent);
        /*
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
                      .setSmallIcon(R.drawable.notification)
                        .setContentTitle("Remote")
//                        .setContentText("Pause")
                        .setDefaults(Notification.DEFAULT_ALL)
                        .addAction (R.drawable.pause,
                                "", pipause)
                        .addAction(R.drawable.revind ,
                                "", piRevind)
                        .addAction (R.drawable.ffw,
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
        mNotificationManager.notify(CommonConstants.NOTIFICATION_ID, builder.build()); */

    }
}