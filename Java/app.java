import java.applet.*;
import java.awt.Graphics;
public class app extends Applet 
{

    public void paint(Graphics g) 
    {
        String str = getParameter("text");
        g.drawString(str, 150,150);
    }
}

/*
<applet code = "app.class" width = "300" height = "300">
<param name ="text" value = "We will overcome from this pandamic"
</applet>
*/
