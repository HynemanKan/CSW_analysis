import os
import time
def get_target_file(need_TW = False):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    for file in os.listdir("res"):
        name = file.split(".")
        if name[1] == "utf8":
            res_address = os.path.join(dir_path,"res",file)
        if os.path.exists(os.path.join(dir_path,"gold",file.replace("res","test_gold"))):
            gold_address = os.path.join(dir_path,"gold",file.replace("res","test_gold"))
        yield res_address,gold_address


def str2li(word_li:list):
    outdata=[[0,0]]
    for i in range(len(word_li)):
        a = len(word_li[i])
        outdata.append([outdata[i][1],outdata[i][1]+a])
    outdata.pop(0)
    return outdata


name =input("res:")
line = 0
for res_address,gold_address in get_target_file():
    print(res_address)
    print(gold_address)
    with open(f"{name}_{line}.txt","w",encoding="utf-8") as log_file:
        with open(res_address,"r",encoding="utf-8") as res_file:
            with open(gold_address,"r",encoding="utf-8") as gold_file:
                N_all =0
                E_all =0
                C_all =0
                while True:
                    res_line =res_file.readline()
                    gold_line = gold_file.readline()
                    if  not(res_line=="stop code\n"):
                        print("\r"+str(line)+"\t"+gold_line.replace("\n",''),end="")
                        temp_res = str2li(res_line.split(" "))
                        temp_gold = str2li(gold_line.split(" "))
                        N = len(temp_gold)
                        CandE = len(temp_res)
                        C = len([val for val in temp_res if val in temp_gold])
                        E = CandE -C
                        R =C/N
                        P = C/CandE
                        ER = E/N
                        try:
                            F = 2*P*R/(P+R)
                        except ZeroDivisionError:
                            F = 0
                        log_file.write(res_line)
                        log_file.write(gold_line)
                        log_file.write(f"{str(temp_res)}\n")
                        log_file.write(f"{str(temp_gold)}\n")
                        log_file.write(f"N={N}\tE={E}\tC={C}\n")
                        log_file.write(f"R={R}\tP={P}\tF={F}\tER={ER}\n")
                        log_file.write("\n\n")
                        N_all += N
                        E_all += E
                        C_all += C
                        line+=1
                    else:
                        break
                R_all = C_all / N_all
                try:
                    P_all = C_all / (C_all+E_all)
                except ZeroDivisionError:
                    P_all = "ZeroDivisionError"
                ER_all = E_all / N_all
                try:
                    F_all = 2 * P_all * R_all / (P_all + R_all)
                except Exception as e:
                    F_all = str(e)
                log_file.write(f"{'*'*10}\n")
                log_file.write(f"N_all={N_all}\tE_all={E_all}\tC_all={C_all}\n")
                log_file.write(f"R_all={R_all}\tP_all={P_all}\tF_all={F_all}\tER_all={ER_all}\n")


