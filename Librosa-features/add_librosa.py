import sys
import numpy
import librosa
import json


def get_librosa(path):
  
    #Load an audio file as a floating point time series

    y, sr = librosa.load(path)

    # Decompose an audio time series into harmonic and percussive components

    y_harmonic, y_percussive = librosa.effects.hpss(y)

    # -------------BEAT AND TEMPO--------------------
    
    # Compute a spectral flux onset strength envelope

    hop_length = 512
    onset_env = librosa.onset.onset_strength(y = y_percussive, sr = sr, aggregate = numpy.median,  hop_length=hop_length)
  
    # Dynamic programming beat tracker  
    
    tempo, beats = librosa.beat.beat_track(onset_envelope = onset_env, sr = sr)
    
    # Compute the tempogram: local autocorrelation of the onset strength envelope.

    tempogram = librosa.feature.tempogram(onset_envelope = onset_env, sr = sr, hop_length = hop_length)
    # Median-aggregation by beats
    tempo_b = librosa.feature.sync(tempogram, beats, aggregate = numpy.median)
    
    
    #--------------SPECTRAL FEATURES----------------

    # Compute a chromagram from a waveform or power spectrogram
    
    chroma = librosa.feature.chroma_stft(y = y_harmonic, sr = sr)

    # Beat-synchronous chroma (median aggregation)

    chroma_sync = librosa.feature.sync(chroma, beats, aggregate = numpy.median)

    # Compute a Mel-scaled power spectrogram

    mel = librosa.feature.melspectrogram(y = y, sr = sr)

    # Convert to log scale (dB). We'll use the peak power as reference.

    log_mel = librosa.logamplitude(mel, ref_power = numpy.max)

    # Median-aggregation by beats

    log_mel_b = librosa.feature.sync(log_mel, beats, aggregate = numpy.median)



    #-------------WRITING TO FILE----------------

    tmp = numpy.round_(onset_env, decimals=3)
    onset_env_w = tmp.tolist()
    
    tmp = numpy.round_(tempo_b, decimals=3)
    tempo_b_w = tmp.tolist()

    tmp = numpy.round_(chroma_sync, decimals=3)
    chroma_sync_w = tmp.tolist()

    tmp = numpy.round_(log_mel_b, decimals=3)
    mel_w = tmp.tolist()

    features_dict = {"Tempo": tempo, "Onset strength envelope": onset_env_w,
                     "Beat-synchronous tempogram": tempo_b_w,
                     "Beat-synchronous chroma": chroma_sync_w,
                     "Beat-synchronous log-scaled melspectrogram": mel_w}

    
    suf_ind = path.find(".")

    if (suf_ind != -1):
        file_name = path[0:suf_ind] + "_librosa.json"
    else:
        file_name = path + "_librosa.json"


    with open(file_name, 'w') as f:
         f.write(json.dumps(features_dict))        

    f.close()   

    return





def get_librosa_large(path):
  
    #Load an audio file as a floating point time series

    y, sr = librosa.load(path)

    # Decompose an audio time series into harmonic and percussive components

    y_harmonic, y_percussive = librosa.effects.hpss(y)

    # -------------BEAT AND TEMPO--------------------
    
    # Compute a spectral flux onset strength envelope

    hop_length = 512
    onset_env = librosa.onset.onset_strength(y = y_percussive, sr = sr, aggregate = numpy.median,  hop_length=hop_length)

    # Dynamic programming beat tracker  
    
    tempo, beats = librosa.beat.beat_track(onset_envelope = onset_env, sr = sr)

    # Locate note onset events by picking peaks in an onset strength envelope
    
    onset_frames = librosa.onset.onset_detect(onset_envelope = onset_env, sr = sr)

    
    # Compute the tempogram: local autocorrelation of the onset strength envelope.

    tempogram = librosa.feature.tempogram(onset_envelope = onset_env, sr = sr, hop_length = hop_length)

    #--------------SPECTRAL FEATURES----------------

    # Compute a chromagram from a waveform or power spectrogram
    
    chroma = librosa.feature.chroma_stft(y = y_harmonic, sr = sr)

    # Compute a Mel-scaled power spectrogram

    mel = librosa.feature.melspectrogram(y = y, sr = sr)
    mel_h = librosa.feature.melspectrogram(y = y_harmonic, sr = sr)
    mel_p = librosa.feature.melspectrogram(y = y_percussive, sr = sr)

    # Convert to log scale (dB). We'll use the peak power as reference.

    log_mel = librosa.logamplitude(mel, ref_power = numpy.max)
    log_mel_h = librosa.logamplitude(mel_h, ref_power = numpy.max)
    log_mel_p = librosa.logamplitude(mel_p, ref_power = numpy.max)    

    # Mel-frequency cepstral coefficients

    mfcc = librosa.feature.mfcc(S = log_mel)
    delta_mfcc  = librosa.feature.delta(mfcc)
    delta2_mfcc = librosa.feature.delta(mfcc, order=2)

    # Compute root-mean-square (RMS) energy for each frame

    S, phase = librosa.magphase(chroma)
    rms = librosa.feature.rmse(S = S)
    
    # Compute the spectral centroid
    
    cent = librosa.feature.spectral_centroid(S = S)

    # Compute p’th-order spectral bandwidth

    spec_bw = librosa.feature.spectral_bandwidth(S = S)

    # Compute spectral contrast

    S_abs = numpy.abs(chroma)
#    contrast = librosa.feature.spectral_contrast(S = S_abs, sr = sr)
    
    # Compute roll-off frequency

    rolloff = librosa.feature.spectral_rolloff(S = S, sr = sr)

    # Get coefficients of fitting an nth-order polynomial to the columns of a spectrogram
    
    line = librosa.feature.poly_features(S = S_abs, sr = sr)
    quad = librosa.feature.poly_features(S = S_abs, order = 2)

    # Compute the zero-crossing rate of an audio time series
    
    z_cross = librosa.feature.zero_crossing_rate(y)


    #-------------WRITING TO FILE----------------
    
    features = [tempo, onset_env, beats, onset_frames, tempogram, chroma, log_mel, log_mel_h, log_mel_p, mfcc,
                delta_mfcc, delta2_mfcc, rms, cent, spec_bw, rolloff, line, quad, z_cross]

    features_names = ["Tempo", "Onset strength envelope", "Beats", "Onset events", "Tempogram", "Chromagram",
                      "Log-scaled melspectrogram", "Log-scaled harmonic melspectrogram",
                      "Log-scaled percussive melspectrogram", "Mel-frequency cepstral coefficients", "Delta features",
                      "Delta square features", "Root mean square energy", "Spectral centroid", "Spectral bandwidth",
                      "Roll-off frequency", "Linear coefficients", "Quadratic coefficients", "Zero crossing rate"]

    
    suf_ind = path.find(".")

    if (suf_ind != -1):
        file_name = path[0:suf_ind] + ".dat"
    else:
        file_name = path + ".dat"


    with open(file_name, 'w') as f:
        
        tmp = "%s : %s\n" % (features_names[0], str(features[0]))     # Tempo
        f.write(tmp)
        
        for i in range(1, len(features)):

            tmp = "%s : %s\n" % (features_names[i], str(features[i].tolist()))
            f.write(tmp)         

    f.close()    

    return



        
        

    
