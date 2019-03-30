# -*- coding:utf-8 -*-


def e(a, b, c):
    """

    function(a, b, c) {
        var e, g, h, i, j, k, l, m, n, d = "", f = "", o = window.parseInt;
        for (e in a)
            if (e.indexOf(b) > 0 && a[e].length == o(c)) {
                d = a[e];
                break
            }
        if (d) {
            for (f = "",
            g = 1; g < d.length; g++)
                f += o(d[g]) ? o(d[g]) : 1;
            for (j = o(f.length / 2),
            k = o(f.substring(0, j + 1)),
            l = o(f.substring(j)),
            g = l - k,
            g < 0 && (g = -g),
            f = g,
            g = k - l,
            g < 0 && (g = -g),
            f += g,
            f *= 2,
            f = "" + f,
            i = o(c) / 2 + 2,
            m = "",
            g = 0; g < j + 1; g++)
                for (h = 1; h <= 4; h++)
                    n = o(d[g + h]) + o(f[g]),
                    n >= i && (n -= i),
                    m += n;
            return m
        }
        return d
    }
    """
    d = ""
    for e in a:
        if e.count(b) > 0 and len(a[e]) == c:
            d = a[e]
            break

    if d:
        f = ""
        for g in d[1:]:
            f += "1" if g == "0" else g
        j = int(len(f)/2)
        k = int(f[0:j+1])
        l = int(f[j:])
        g = abs(l-k)
        f = g
        f += g
        f *= 2
        f = str(f)
        i = int(c)//2 + 2
        m = ""
        for g in range(j+1):
            for h in range(1, 5):
                n = int(d[g+h]) + int(f[g])
                if n >=i:
                    n -= i
                m += str(n)
        return m
    return d


def parse(a, b="function/", c="code", d=16):
    """
    function(a, b, c, d, e) {
    for (var f in a)
        if (0 == a[f].indexOf(b)) {
            var g = a[f].substring(b.length).split(b[b.length - 1]);
            if (g[0] > 0) {
                var h = g[6].substring(0, 2 * parseInt(d))
                  , i = e ? e(a, c, d) : "";
                if (i && h) {
                    for (var j = h, k = h.length - 1; k >= 0; k--) {
                        for (var l = k, m = k; m < i.length; m++)
                            l += parseInt(i[m]);
                        for (; l >= h.length; )
                            l -= h.length;
                        for (var n = "", o = 0; o < h.length; o++)
                            n += o == k ? h[l] : o == l ? h[k] : h[o];
                        h = n
                    }
                    g[6] = g[6].replace(j, h),
                    g.splice(0, 1),
                    a[f] = g.join(b[b.length - 1])
                }
            }
        }
}
    d: 16
    c: code
    a: {}
    b: function/
    :return:
    """
    for f in a:
        if a[f].startswith(b):
            g = a[f][len(b):].split("/")
            h = g[6][:2*d]
            i = e(a, c, d)
            if i and h:
                j = h
                for k in range(len(h)-1, -1, -1):
                    l = k
                    for m in range(k, len(i)):
                        l += int(i[m])
                    while l >= len(h):
                        l -= len(h)
                    n = ""
                    for o in range(len(h)):
                        n += h[l] if o == k else (h[k] if o == l else h[o])
                    h = n
                g[6] = g[6].replace(j, h)
                g = g[1:]
                a[f] = "/".join(g)



if __name__ == "__main__":
    import json
    a = json.loads('{"video_alt_url":"function/232/http://seku.tv/get_file/1/e08d1f6ea524f26f04bde2a5d7107259f548bdcda0/6000/6006/6006_480p.mp4/?embed=true","embed_mode":"1","video_id":"6006","license_code":"$305304810072540","lrc":"40717880","rnd":"1524337601","video_url":"http://seku.tv/get_file/1/699f42c84107dc37aa44d934f6c0ecdf372ac1bf52/6000/6006/6006_360p.mp4/?embed=true","postfix":"_360p.mp4","video_url_text":"360 P","_video_alt_url":"function/232/http://seku.tv/get_file/1/e08d1f6ea524f26f04bde2a5d7107259f548bdcda0/6000/6006/6006_480p.mp4/?embed=true","video_alt_url_text":"480 P","default_slot":"2","timeline_screens_url":"http://seku.tv/contents/videos_screenshots/6000/6006/timelines/360p/200x116/{time}.jpg","timeline_screens_interval":"10","preview_url":"http://seku.tv/contents/videos_screenshots/6000/6006/preview_480p.mp4.jpg","skin":"youtube.css","bt":"3","volume":"1","hide_controlbar":"1","hide_style":"fade","disable_preview_resize":"true","embed":"1"}')
    #print(e(a, "code", 16))
    parse(a)
    print(a)