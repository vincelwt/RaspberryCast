package com.example.aditya.picast;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.EditText;
import android.widget.Toast;


public class MainActivity extends Activity {

    private String  url="";
    private String ip ="";
    private String IPsettings = "settings";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Log.d("MAIN", "OnCreated");
        SharedPreferences settings = getSharedPreferences(getIPsettings(),MODE_PRIVATE);
        setIp(settings.getString(IPsettings,"Not Available"));
        ip = settings.getString(getIPsettings(), "Not Available");
        final String notavailable = "<html><title>Server name not Valid</title><body><h2>The IP Address is not Valid</h2><p>The IP Address is invalid or not entered at all</p><p>If you have not set it yet, please go to the <b>Settings</b> and set the IP Address of your Raspberry Pi</p></body></html>";
        setUrl("http://" + getIp() + ":2020/remote");
        WebView remote = (WebView) findViewById(R.id.remote);

        remote = (WebView) findViewById(R.id.remote);
        remote.setVerticalScrollBarEnabled(true);
        remote.setHorizontalScrollbarOverlay(true);
        remote.getSettings().setJavaScriptEnabled(true);

        if(getIp() != "Not Available" ) {


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
                    Log.d("WebView", "Not F***ING found");
                    finalRemote.loadData(notavailable, "text/html", null);
                }
            });
        }
        else if(getIp() == "Not Available"){ Log.d("WebView","Not Available"); remote.loadData(notavailable, "text/html", null);}

    }





    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        // int id = item.getItemId();
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

                //setContentView(R.layout.activity_settings);
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
}
