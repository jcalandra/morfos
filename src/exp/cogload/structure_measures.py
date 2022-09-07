import mir_eval
from data_processing import list2intervals


def segs_per_song(data):
    segmentations = [[] for i in range(len(data[0][0]))]
    for sujet in data:
        for s in range(len(sujet[0])):
            segmentations[s].append(sujet[0][s])


def compute_segs_accuracy(segs, data):
    segmentation_stats = []
    for sujet in data:
        for s in range(len(sujet[0][:16])):
            if s % 2 == 0:
                est_list_phrase = sujet[0][s]
                est_list_section = sujet[0][s + 1]
                est_intervals_phrase = list2intervals(est_list_phrase)
                est_intervals_section = list2intervals(est_list_section)

                seg_song = []
                for seg in range(len(segs[s//2])):
                    if seg % 2 == 0:
                        ref_list_phrase = segs[s//2][seg]
                        ref_list_section = segs[s//2][seg + 1]
                        ref_intervals_phrase = list2intervals(ref_list_phrase)
                        ref_intervals_section = list2intervals(ref_list_section)

                        windows = [500, 1000, 3000]
                        seg_stats = []
                        for w in windows:
                            pwp, rwp, fwp = mir_eval.segment.detection(ref_intervals_phrase, est_intervals_phrase,
                                                                       window=w, beta=1.0, trim=False)
                            pws, rws, fws = mir_eval.segment.detection(ref_intervals_section, est_intervals_section,
                                                                       window=w, beta=1.0, trim=False)
                            seg_stats.append(["P"+str(w)+"p", pwp])
                            seg_stats.append(["R"+str(w)+"p", rwp])
                            seg_stats.append(["F"+str(w)+"p", fwp])
                            seg_stats.append(["P"+str(w)+"s", pws])
                            seg_stats.append(["R"+str(w)+"s", rws])
                            seg_stats.append(["F"+str(w)+"s", fws])

                        r2ep, e2rp = mir_eval.segment.deviation(ref_intervals_phrase, est_intervals_phrase)
                        r2es, e2rs = mir_eval.segment.deviation(ref_intervals_section, est_intervals_section)
                        seg_stats.append(["r2ep", r2ep])
                        seg_stats.append(["e2rp", e2rp])
                        seg_stats.append(["r2es", r2es])
                        seg_stats.append(["e2rs", e2rs])
                        seg_song.append(seg_stats)
                    if seg % 2 == 1:
                        pass
                segmentation_stats.append(seg_song)
    return segmentation_stats

