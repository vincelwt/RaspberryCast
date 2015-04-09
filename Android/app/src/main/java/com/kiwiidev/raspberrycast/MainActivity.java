package com.kiwiidev.raspberrycast;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.NotificationManager;
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
import android.widget.Toast;

import com.kiwiidev.raspberrycast.R;


public class MainActivity extends Activity {

    private String  url="";
    private String ip ="";
    private String IPsettings = "settings";
    final String notavailable = "<html><title>Oops...</title><body><h2>Oops...</h2><p>I couldn't access the server.</p><p>Please make sure :<ul><li><b>The IP Address of your Raspberry Pi is correct</li><li>The RaspberryCast server is running on your Raspberry Pi</li><li>You are on the same network as your Raspberry Pi</li></b></ul></p></body></html>";
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

                userInput.setText(CommonConstants.IP);

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
                        .setNegativeButton(getString(R.string.cancel),new DialogInterface.OnClickListener() {
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
    }
    public void setUrl(String url) {
        this.url = url;
    }
    public String getIp() {

        return ip;
    }
    public void setIp(String ip) {

        this.ip = ip;
    }
    public String getIPsettings() {
        return IPsettings;
    }
    public void setIPsettings(String IPsettings) {

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
                .setNegativeButton(getString(R.string.cancel),new DialogInterface.OnClickListener() {
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
        mServiceIntent.putExtra(CommonConstants.IP,getIp());
        if(stats == true) {
            mServiceIntent.setAction(CommonConstants.ACTION_START);
        } else if (stats == false){
            mServiceIntent.setAction(CommonConstants.ACTION_STOP);
        }
        startService(mServiceIntent);
    }
}