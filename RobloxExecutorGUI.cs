using System;
using System.Runtime.InteropServices;
using System.Windows.Forms;

public class RobloxExecutorGUI : Form
{
    // Import C++ functions
    [DllImport("RobloxExecutor.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern IntPtr create_executor();

    [DllImport("RobloxExecutor.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern void destroy_executor(IntPtr executor);

    [DllImport("RobloxExecutor.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern bool authenticate_executor(IntPtr executor, string cookie, string placeId);

    [DllImport("RobloxExecutor.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern bool execute_script(IntPtr executor, string script);

    private TextBox txtCookie;
    private TextBox txtPlaceId;
    private TextBox txtScript;
    private TextBox txtOutput;
    private Button btnExecute;
    private Button btnClear;
    private Button btnExample;
    private IntPtr executorPtr;

    public RobloxExecutorGUI()
    {
        InitializeComponent();
        executorPtr = create_executor();
    }

    private void InitializeComponent()
    {
        this.Text = "Roblox Executor";
        this.Size = new System.Drawing.Size(800, 600);
        this.StartPosition = FormStartPosition.CenterScreen;

        // Cookie input
        Label lblCookie = new Label();
        lblCookie.Text = "ROBLOSECURITY Cookie:";
        lblCookie.Location = new System.Drawing.Point(10, 10);
        lblCookie.Size = new System.Drawing.Size(150, 20);

        txtCookie = new TextBox();
        txtCookie.Location = new System.Drawing.Point(10, 30);
        txtCookie.Size = new System.Drawing.Size(760, 20);

        // Place ID input
        Label lblPlaceId = new Label();
        lblPlaceId.Text = "Place ID:";
        lblPlaceId.Location = new System.Drawing.Point(10, 60);
        lblPlaceId.Size = new System.Drawing.Size(100, 20);

        txtPlaceId = new TextBox();
        txtPlaceId.Location = new System.Drawing.Point(10, 80);
        txtPlaceId.Size = new System.Drawing.Size(760, 20);

        // Script input
        Label lblScript = new Label();
        lblScript.Text = "Lua Script:";
        lblScript.Location = new System.Drawing.Point(10, 110);
        lblScript.Size = new System.Drawing.Size(100, 20);

        txtScript = new TextBox();
        txtScript.Multiline = true;
        txtScript.ScrollBars = ScrollBars.Vertical;
        txtScript.Location = new System.Drawing.Point(10, 130);
        txtScript.Size = new System.Drawing.Size(760, 200);
        txtScript.Text = "-- Enter your Lua script here\nprint('Hello, Roblox!')";

        // Buttons
        btnExecute = new Button();
        btnExecute.Text = "Execute Script";
        btnExecute.Location = new System.Drawing.Point(10, 340);
        btnExecute.Size = new System.Drawing.Size(100, 30);
        btnExecute.Click += BtnExecute_Click;

        btnClear = new Button();
        btnClear.Text = "Clear Output";
        btnClear.Location = new System.Drawing.Point(120, 340);
        btnClear.Size = new System.Drawing.Size(100, 30);
        btnClear.Click += BtnClear_Click;

        btnExample = new Button();
        btnExample.Text = "Load Example";
        btnExample.Location = new System.Drawing.Point(230, 340);
        btnExample.Size = new System.Drawing.Size(100, 30);
        btnExample.Click += BtnExample_Click;

        // Output
        Label lblOutput = new Label();
        lblOutput.Text = "Output:";
        lblOutput.Location = new System.Drawing.Point(10, 380);
        lblOutput.Size = new System.Drawing.Size(100, 20);

        txtOutput = new TextBox();
        txtOutput.Multiline = true;
        txtOutput.ScrollBars = ScrollBars.Vertical;
        txtOutput.ReadOnly = true;
        txtOutput.Location = new System.Drawing.Point(10, 400);
        txtOutput.Size = new System.Drawing.Size(760, 150);

        // Add controls to form
        this.Controls.AddRange(new Control[] {
            lblCookie, txtCookie,
            lblPlaceId, txtPlaceId,
            lblScript, txtScript,
            btnExecute, btnClear, btnExample,
            lblOutput, txtOutput
        });
    }

    private void BtnExecute_Click(object sender, EventArgs e)
    {
        if (string.IsNullOrEmpty(txtCookie.Text) || string.IsNullOrEmpty(txtPlaceId.Text))
        {
            MessageBox.Show("Please enter both ROBLOSECURITY cookie and Place ID.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }

        bool authenticated = authenticate_executor(executorPtr, txtCookie.Text, txtPlaceId.Text);
        if (!authenticated)
        {
            txtOutput.AppendText("Authentication failed!\n");
            return;
        }

        txtOutput.AppendText("Authenticated successfully.\n");
        
        bool result = execute_script(executorPtr, txtScript.Text);
        if (result)
        {
            txtOutput.AppendText("Script executed successfully.\n");
        }
        else
        {
            txtOutput.AppendText("Script execution failed.\n");
        }
    }

    private void BtnClear_Click(object sender, EventArgs e)
    {
        txtOutput.Clear();
    }

    private void BtnExample_Click(object sender, EventArgs e)
    {
        txtScript.Text = @"-- Roblox Executor Example Script
print('Roblox Executor is working!')
game.Players.LocalPlayer.Character.Humanoid.WalkSpeed = 50
game.Players.LocalPlayer.Character.Humanoid.JumpPower = 100";
    }

    protected override void Dispose(bool disposing)
    {
        if (disposing)
        {
            destroy_executor(executorPtr);
        }
        base.Dispose(disposing);
    }

    [STAThread]
    public static void Main()
    {
        Application.EnableVisualStyles();
        Application.SetCompatibleTextRenderingDefault(false);
        Application.Run(new RobloxExecutorGUI());
    }
}