package com.kiwiidev.raspberrycast;

import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.TextView;

import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.StatusLine;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class Queue extends ActionBarActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_cast);

        final TextView txtView = (TextView)findViewById(R.id.txt);
        //get the received intent
        Intent receivedIntent = getIntent();
        //get the action
        String receivedAction = receivedIntent.getAction();
        //find out what we are dealing with
        String receivedType = receivedIntent.getType();
        //make sure it's an action and type we can handle
        if (receivedAction.equals(Intent.ACTION_SEND)){
            //get the received text
            String receivedText = receivedIntent.getStringExtra(Intent.EXTRA_TEXT);
            //check we have a string
            if (receivedText != null) {
                //set the text
                txtView.setText(receivedText);

                String firstlink = extractUrls(receivedText).get(0);

                txtView.setText("Adding to playlist : "+firstlink);

                String url = "http://" + CommonConstants.IP + ":2020/queue?url=" + URLEncoder.encode(firstlink);

                new RequestTask().execute(url);

                Timer t = new Timer();
                t.schedule(new TimerTask() {

                    @Override
                    public void run() {
                        finish();
                    }
                }, 3000);

            }
        }
    }

    private List<String> extractUrls(String value){
        List<String> result = new ArrayList<String>();
        String urlPattern = "((https?|ftp|file):((//)|(\\\\))+[\\w\\d:#@%/;$()~_?\\+-=\\\\\\.&]*)";
        Pattern p = Pattern.compile(urlPattern, Pattern.CASE_INSENSITIVE);
        Matcher m = p.matcher(value);
        while (m.find()) {
            result.add(value.substring(m.start(0),m.end(0)));
        }
        return result;
    }
}
