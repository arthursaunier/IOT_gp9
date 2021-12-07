package com.example.miniprojet_iot;

import static java.lang.Integer.valueOf;

import androidx.appcompat.app.AppCompatActivity;

import android.os.AsyncTask;
import android.os.Bundle;
import android.text.Editable;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Timer;
import java.util.TimerTask;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

public class MainActivity extends AppCompatActivity {

    private String IP;
    private int PORT;
    private InetAddress address;
    private DatagramSocket UDPSocket;
    private DatagramSocket UDPSocketRec;
    private Timer timer;
    public Sync sync;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        EditText EText1 = findViewById(R.id.editTextTextPersonName);
        EditText EText2 = findViewById(R.id.editTextTextPersonName2);
        Button button1 = findViewById(R.id.button1);
        Button button2 = findViewById(R.id.button2);
        Button button3 = findViewById(R.id.button3);
        TextView TView1 = findViewById(R.id.textView1);
        TextView TView2 = findViewById(R.id.textView2);


        try {
            UDPSocket = new DatagramSocket();
        } catch (SocketException e) {
            e.printStackTrace();
        }
        try {
            /*AskUpdate();*/
            sync = new Sync();
            sync.execute();
        } catch (Exception e){
            e.printStackTrace();
        }

        button1.setOnClickListener( new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    if (EText1.getText().toString().isEmpty()){
                        IP = "192.168.1.90";
                    }else{
                        IP = EText1.getText().toString();
                    }
                    if (EText2.getText().toString().isEmpty()){
                        PORT = 10000;
                    }else{
                        PORT = Integer.parseInt(EText2.getText().toString());
                    }
                    address = InetAddress.getByName(IP);
                } catch (UnknownHostException e) {
                    e.printStackTrace();
                }
                String message = "TL";
                DatagramPacket dp = new DatagramPacket(message.getBytes(StandardCharsets.UTF_8), message.length(),address, PORT);
                Executor executor = Executors.newSingleThreadExecutor();
                executor.execute(new Runnable() {
                    @Override
                    public void run() {
                        try {
                            UDPSocket.send(dp);
                            System.out.println("TL envoyé");
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                });
            }
        });

        button2.setOnClickListener( new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    if (EText1.getText().toString().isEmpty()){
                        IP = "192.168.1.90";
                    }else{
                        IP = EText1.getText().toString();
                    }
                    if (EText2.getText().toString().isEmpty()){
                        PORT = 10000;
                    }else{
                        PORT = Integer.parseInt(EText2.getText().toString());
                    }
                    address = InetAddress.getByName(IP);
                } catch (UnknownHostException e) {
                    e.printStackTrace();
                }
                String message = "LT";
                DatagramPacket dp = new DatagramPacket(message.getBytes(StandardCharsets.UTF_8), message.length(),address, PORT);
                Executor executor = Executors.newSingleThreadExecutor();
                executor.execute(new Runnable() {
                    @Override
                    public void run() {
                        try {
                            UDPSocket.send(dp);
                            System.out.println("LT envoyé");
                            System.out.println(dp);
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                });
            }
        });

        button3.setOnClickListener( new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    if (EText1.getText().toString().isEmpty()){
                        IP = "192.168.1.90";
                    }else{
                        IP = EText1.getText().toString();
                    }
                    if (EText2.getText().toString().isEmpty()){
                        PORT = 10000;
                    }else{
                        PORT = Integer.parseInt(EText2.getText().toString());
                    }
                    address = InetAddress.getByName(IP);
                } catch (UnknownHostException e) {
                    e.printStackTrace();
                }
                String message = "update";
                DatagramPacket dp = new DatagramPacket(message.getBytes(StandardCharsets.UTF_8), message.length(),address, PORT);
                Executor executor = Executors.newSingleThreadExecutor();
                executor.execute(new Runnable() {
                    @Override
                    public void run() {
                        try {
                            UDPSocket.send(dp);
                            System.out.println("update envoyé");
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                });
            }
        });

        /*byte[] buf = new byte[1024];
        DatagramPacket dprec = new DatagramPacket(buf, 1024, address, PORT);
        Executor executorrec = Executors.newSingleThreadExecutor();
        executorrec.execute(new Runnable() {
            @Override
            public void run() {
                try {
                    UDPSocketRec.receive(dprec);
                    String data = new String(dprec.getData(), 0, dprec.getLength());
                    String[] valeurs = data.toString().split(":");
                    TView1.setText(valeurs[0] + "°C");
                    TView2.setText(valeurs[1] + "UA");
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });*/

    }

    private class Sync extends AsyncTask<Void, String, Void>{

        TextView TView1 = findViewById(R.id.textView1);
        TextView TView2 = findViewById(R.id.textView2);

        @Override
        protected Void doInBackground(Void... voids) {
            while (true){
                try {
                    System.out.printf("do in back");
                    byte[] buf = new byte[1024];
                    DatagramPacket dprec = new DatagramPacket(buf, buf.length);
                    System.out.println("je suis la ");
                    UDPSocket.receive(dprec);
                    System.out.println(dprec);
                    String data = new String(dprec.getData(), dprec.getOffset(), dprec.getLength());
                    publishProgress(data);
                } catch (IOException e) {
                    System.out.println("erreur");
                    e.printStackTrace();

                }
            }
        }

        protected void onProgressUpdate(String... data) {
            super.onProgressUpdate(data);
            System.out.println("on progress");
            System.out.println(data.toString());
            System.out.println(data);
            String[] valeurs = data.toString().split(":");
            TView1.setText(/*valeurs[0]*/  "°C");
            TView2.setText(/*valeurs[1] */ "UA");
        }
    }


    /*private void AskUpdate() {
        TextView TView1 = findViewById(R.id.textView1);
        TextView TView2 = findViewById(R.id.textView2);
        EditText EText1 = findViewById(R.id.editTextTextPersonName);
        EditText EText2 = findViewById(R.id.editTextTextPersonName2);
        timer = new Timer();

        timer.scheduleAtFixedRate( new TimerTask() {
            public void run() {

                System.out.println("timer lancé");

                try{
                    if (EText1.getText().toString().isEmpty()){
                        IP = "192.168.1.90";
                    }else{
                        IP = EText1.getText().toString();
                    }
                    if (EText2.getText().toString().isEmpty()){
                        PORT = 10000;
                    }else{
                        PORT = Integer.parseInt(EText2.getText().toString());
                    }
                    address = InetAddress.getByName(IP);

                    String message = "update";
                    DatagramPacket dpu = new DatagramPacket(message.getBytes(StandardCharsets.UTF_8), message.length(),address, PORT);
                    Executor executoru = Executors.newSingleThreadExecutor();
                    executoru.execute(new Runnable() {
                        @Override
                        public void run() {
                            try {
                                UDPSocket.send(dpu);
                                System.out.println("update envoyé");
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                        }
                    });


                }
                catch (Exception e) {
                    e.printStackTrace();
                }

            }
        }, 5000, 10000);
    }*/

}