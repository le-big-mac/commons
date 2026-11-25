"""build-readme.py -- fill README.src.md (with found.md and limits.md inside it) from facts.json, setting.json and fill.json.
usage: python -I build-readme.py"""
import json, re
F = json.load(open("facts.json")); S = json.load(open("setting.json")); fill = json.load(open("fill.json"))
def commas(n): return "{:,}".format(int(n))
T = dict(fill)
T.update(NX=S["NX"], NY=S["NY"], KL=S["KL"], bank_pct="%g" % (100 * S["KL"] * 0.05), film_seconds=24, grown_steps=commas(600000),
         grown_streams=F["grown_streams"], grown_wet=F["grown_wet"], grown_relief=F["grown_relief"])
e = {r[0]: r for r in F["early"]}; T.update(e1_streams=e[100000][1], e1_wet=e[100000][2], e3_streams=e[300000][1], e3_wet=e[300000][2])
T.update(smooth_relief=F["smooth_relief"], smooth_last=commas(F["smooth_last"]), gentle_capped_relief=F["gentle_capped_relief"])
assert F["smooth_maxstreams"] == 1.0 and F["smooth_minwet"] == 100 and F["smooth_capped_maxstreams"] == 1.0 and F["gentle_capped_maxstreams"] == 1.0
T.update(n1_streams=F["small_n1"][1], n1_wet=F["small_n1"][2], k0_top=F["small_k0"][3], k0_wet=F["small_k0"][2], m1_relief=F["small_m1"][4], m1_last=commas(F["small_m1"][0]))
T.update(after_kl0_last=commas(F["after_kl0_last"]), after_kl0_streams=F["after_kl0_streams"], after_kl0_wet=F["after_kl0_wet"], after_kl0_top=F["after_kl0_top"], after_kl0_relief=F["after_kl0_relief"])
T.update(fade_half=commas(F["fade_half"]), fade_one=commas(F["fade_one"]), fade_sheet=commas(F["fade_sheet"]))
T.update(table_fixed=F["table_fixed"], table_other=F["table_other"])
cut, times, ratio = F["supply_cut"], F["supply_times"], F["supply_ratio"]      # the first entry of each is the 600,000-step bed, the other four the beds at 4 million
T.update(cut_600k="%.1f" % -cut[0], cut_lo="%.1f" % min(-x for x in cut[1:]), cut_hi="%.1f" % max(-x for x in cut[1:]), times_lo="%.1f" % min(times[1:]), times_hi="%.1f" % max(times[1:]),
         ratio_lo="%.1f" % min(ratio[1:]), ratio_hi="%.1f" % max(ratio[1:]), longest_ratio=int(4000000 / 181000), limit_pct=3)
T.update(lim_relief=F["limit01_relief"], lim_time=commas(F["limit01_time"]), ref_relief_lo=min(F["limit_ref"]), ref_relief_hi=max(F["limit_ref"]))
T.update(smooth_looks=F["smooth_looks"], n1_300_wet=F["n1_300_wet"], lim_m2="%.1f" % F["limit01_m2"][2], ref_m2_lo="%.1f" % min(F[k + "_m2"][2] for k in ("kl04", "kl04s2", "kl02", "kl08")), ref_m2_hi="%.1f" % max(F[k + "_m2"][2] for k in ("kl04", "kl04s2", "kl02", "kl08")))
assert F["smooth_after_max"] == F["smooth_after_min"] == F["smooth_relief"]
T.update(up_cells_lo=min(F["up_cells"]), up_cells_hi=max(F["up_cells"]), up_water_lo=min(F["up_water"]), up_water_hi=max(F["up_water"]), capped_steps=commas(F["capped_steps"]))
assert F["capped_always"]
T.update(r15=F["rough1.5"][0], r20=F["rough2"][0], r25=F["rough2.5"][0])
assert F["rough1"][3] == 1.0 and F["rough1"][4] == 100 and F["ditch"][3] == 1.0 and F["ditch"][4] == 100 and F["ditch"][5] <= 0.01 and F["ditch"][6] == 50000 and F["ditch"][7] == 600000
assert all(F["rough" + a][0] > 3 and F["rough" + a][1] < 70 for a in ("1.5", "2", "2.5"))
# ---- after the referee
D = F["draws"]; assert len(D) == 10 and D[0][1] == max(d[1] for d in D) and D[0][2] == min(d[2] for d in D)       # the page's river is the wettest and the least rough of the ten
T.update(draw_streams_lo="%.1f" % min(d[0] for d in D), draw_streams_hi="%.1f" % max(d[0] for d in D), draw_wet_lo=min(d[1] for d in D), draw_wet_hi=max(d[1] for d in D), draw_rough_lo="%.1f" % min(d[2] for d in D), draw_rough_hi="%.1f" % max(d[2] for d in D))
L = {(x["cs"], x["bed"]): x for x in F["linear"]}; pg, lg, l30 = L[(0.05, "page")], L[(0.05, "long")], L[(1.5, "long")]
assert pg["grow"] == 0 and lg["grow"] == 0 and L[(0.5, "long")]["grow"] == 0 and l30["grow"] > 0 and max(x["within"] for x in F["linear"]) < 2e-3
T.update(page_shapes=pg["shapes"], page_slowest="%.4f" % pg["greatest"], long_shapes=lg["shapes"], long_slowest="%.4f" % lg["greatest"], grow30=l30["grow"], ripple_30="%.4f" % l30["greatest"],
         raw2_small="%.3f" % pg["raw"][0], raw2_big="%.3f" % pg["raw"][1], net2="%.4f" % pg["raw"][2])
assert pg["raw"][2] == pg["raw"][3] and pg["raw"][0] > 0.3 and abs(pg["raw"][1]) < 0.01
T.update(kl0_last3="%.2f, then %.2f, then %.2f" % tuple(F["kl0_last3"]))
c6, c15 = F["refCnoon"]; assert c6[0] == 600000 and c15[0] == 1500000
T.update(rc_streams="%.1f" % c15[1], rc_wet="%.0f" % c15[2], rc_top="%.0f" % c15[3], rc_rough="%.1f" % c15[4], rc6_streams="%.1f" % c6[1], rc6_wet="%.0f" % c6[2])
ro = F["refC"]; assert ro[0] == 1200000; T.update(ro_streams="%.1f" % ro[1], ro_wet="%.0f" % ro[2])
T.update(t4_lo="%.1f" % min(F["t4"]), t4_hi="%.1f" % max(F["t4"]))
A = F["refA"]; assert A["n2"] == 5
T.update(ra6_streams="%.1f" % A["s6"], ra6_wet="%.0f" % A["w6"], ra2_streams="%.1f" % A["s2"], ra2_wet="%.0f" % A["w2"], ra_wet_lo="%.0f" % A["wlo"], ra_wet_hi="%.0f" % A["whi"], rb6_streams="%.1f" % A["sB"], rb6_wet="%.0f" % A["wB"])
T.update(div200="%.2f" % F["diverge"][0], div5000="%.1f" % F["diverge"][1], soak_first_streams=F["grown_streams"], soak_first_wet=F["grown_wet"], soak_last_streams=F["soak_last_streams"], soak_last_wet=F["soak_last_wet"])
T.update(ratio_600k="%.2f" % ratio[0], times_600k="%.1f" % times[0])
B = F["budget"]; e = lambda n: B["fate/%s-end.bed" % n]
def signed(x, fmt="%.2f"): return ("+" if x > 0 else "\u2212") + fmt % abs(x)
T.update(bud_kl04="%.2f" % e("kl04")[0], bud_kl04s2=signed(e("kl04s2")[0]), bud_kl02=signed(e("kl02")[0]), bud_kl08=signed(e("kl08")[0]), q_kl04=", ".join(signed(x, "%.1f") for x in e("kl04")[1]),
         low_lo="%.0f" % min(-e(n)[2] for n in ("kl04", "kl04s2", "kl02", "kl08")), low_hi="%.0f" % max(-e(n)[2] for n in ("kl04", "kl04s2", "kl02", "kl08")))
assert e("kl04")[0] > 2 and abs(e("kl04s2")[0]) < 0.5 and e("kl02")[0] < -5 and e("kl08")[0] < -5
k = F["lk02"]; T.update(lk02_a=k[0], lk02_b="%d to %d%%" % (k[1], k[2]), lk02_c="%d to %d%%" % (k[3], k[4]))
T.update(t_loop_lo=commas(min(F["t2_loop"])), t_loop_hi=commas(max(F["t2_loop"])), t_fix_lo=commas(min(F["t2_fixed"])), t_fix_hi=commas(max(F["t2_fixed"])))
r2 = F["refA2t"]; assert r2[0][0] == 450000 and r2[1][0] == 600000
T.update(r2t_rough_a="%.2f" % r2[0][2], r2t_time_a=commas(round(r2[0][1])), r2t_rough_b="%.2f" % r2[1][2], r2t_time_b=commas(round(r2[1][1])))
T.update(table_blind=F["table_blind"])
fm = F["fix_m2"]; assert F["cs01_sheet"]
T.update(cs03_cell=F["cs03_cell"], cs01_looks=F["cs01_looks"], fix_lo_hi="%.1f to %.1f / %d to %d%% / %.1f to %.1f" % (min(x[0] for x in fm), max(x[0] for x in fm), round(min(x[1] for x in fm)), round(max(x[1] for x in fm)), min(x[2] for x in fm), max(x[2] for x in fm)))
T.update(tests_n=int(F["tests"].split()[0]), page_same=F["page_same"], page_rate=F["page_rate"], soak_minutes=F["soak_minutes"], soak_steps=commas(F["soak_last"] - 600000),
         soak_heap=" to ".join(str(x) for x in F["soak_heap"]), quotes=F["quotes"].replace(" found", ""))
assert F["tests"].endswith("0 fail") and F["page_errors"] == "[]" and "script errors []" in F["soak_end"] and "no advance 0" in F["soak_end"]
src = open("README.src.md").read().replace("{{FOUND}}", open("found.md").read().rstrip()).replace("{{LIMITS}}", open("limits.md").read().rstrip())
def sub(m):
    k = m.group(1); assert k in T, "no value for " + k; return str(T[k])
out = re.sub(r"\{\{([A-Za-z0-9_-]+)\}\}", sub, src); out = re.sub(r"\{\{([A-Za-z0-9_-]+)\}\}", sub, out); assert "{{" not in out
open("README.md", "w").write(out); print("README.md", len(out.split()), "words")
json.dump({k: str(v) for k, v in T.items()}, open("tokens.json", "w"), indent=1)      # the same values, for the notes on the page (build.py)
