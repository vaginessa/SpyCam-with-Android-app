package com.example.okla.spycam;

import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.Switch;
import android.widget.Toast;
import java.io.IOException;
import java.net.Socket;
import java.net.UnknownHostException;
import java.io.PrintWriter;
public class MainActivity extends AppCompatActivity {

    public String massage;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Button button2 = findViewById(R.id.button2);

        final Switch switch1 = findViewById(R.id.switch1); //zalacznik
        final Switch switch2 = findViewById(R.id.switch2); //video
        final Switch switch3 = findViewById(R.id.switch3); //zdjecia

        final EditText editTextConnect = findViewById(R.id.editText);
        final EditText editTextEmail = findViewById(R.id.editText3);
        final EditText editTextLiczbaZdj = findViewById(R.id.editText5);

        switch1.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {

            }
        });
        switch2.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                switch3.setChecked(false);
            }
        });

        switch3.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                switch2.setChecked(false);
            }
        });


        button2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String IP = editTextConnect.getText().toString();
                String mail = editTextEmail.getText().toString();
                String number = editTextLiczbaZdj.getText().toString();
                String option;
                String attachm;
                String neww = "1";
                if(switch2.isChecked()){
                    option = "video";
                }else{
                    option = "picture";
                }
                if(switch1.isChecked()){
                    attachm = "1";
                }else{
                    attachm = "0";
                }
                String text =mail+" "+option+" "+number+" "+attachm+" "+ neww;
                //editTextConnect.setText(text);
                send sendcode = new send();
                massage = text;
                sendcode.execute();

            }
        });


    }
    class send extends AsyncTask<Void,Void,Void>{
        Socket socket;
        PrintWriter printWriter;
        @Override
        protected Void doInBackground(Void... voids) {
                try{
                    socket = new Socket("raspberrypi",8000);
                    printWriter = new PrintWriter(socket.getOutputStream());
                    printWriter.write(massage);
                    printWriter.flush();
                    printWriter.close();
                    socket.close();
                } catch (UnknownHostException e) {
                    e.printStackTrace();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                return null;
            }
        }
    }


